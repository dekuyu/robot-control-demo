"""
认证服务模块
JWT 生成/校验、密码验证、锁号逻辑
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole
from app.core.security import (
    verify_password, hash_password,
    create_access_token, create_refresh_token, decode_token,
)
from app.core.exceptions import (
    AuthenticationError, AccountLockedError, PermissionDeniedError,
)
from app.config import settings


async def authenticate_user(
    db: AsyncSession,
    username: str,
    password: str,
) -> dict:
    """
    用户登录认证

    Args:
        db: 数据库会话
        username: 用户名
        password: 明文密码

    Returns:
        包含 access_token, refresh_token, user 的字典

    Raises:
        AuthenticationError: 用户名或密码错误
        AccountLockedError: 账号被锁定
    """
    # 查找用户
    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise AuthenticationError("用户名或密码错误")

    # 检查锁定状态
    if user.is_locked:
        if user.locked_until and user.locked_until > datetime.now(timezone.utc):
            raise AccountLockedError()
        else:
            # 锁定时间已过，自动解锁
            user.is_locked = False
            user.failed_login_attempts = 0
            user.locked_until = None
            await db.flush()

    # 验证用户是否启用
    if not user.is_active:
        raise AuthenticationError("账号已被禁用")

    # 验证密码
    if not verify_password(password, user.password_hash):
        user.failed_login_attempts += 1
        if user.failed_login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
            user.is_locked = True
            user.locked_until = datetime.now(timezone.utc) + timedelta(
                minutes=settings.LOGIN_LOCK_MINUTES
            )
            await db.flush()
            raise AccountLockedError()
        await db.flush()
        raise AuthenticationError("用户名或密码错误")

    # 登录成功，重置失败计数
    user.failed_login_attempts = 0
    user.last_login = datetime.now(timezone.utc)
    await db.flush()

    # 生成 Token
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "user": user,
    }


async def refresh_access_token(
    db: AsyncSession,
    refresh_token: str,
) -> dict:
    """
    刷新 Access Token

    Args:
        db: 数据库会话
        refresh_token: 刷新令牌

    Returns:
        新的 token 信息
    """
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise AuthenticationError("无效的刷新令牌")

    user_id = int(payload.get("sub"))
    user = await get_user_by_id(db, user_id)
    if not user or not user.is_active:
        raise AuthenticationError("用户不存在或已禁用")

    new_access = create_access_token(user_id)
    new_refresh = create_refresh_token(user_id)

    return {
        "access_token": new_access,
        "refresh_token": new_refresh,
        "token_type": "Bearer",
    }


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """根据 ID 获取用户"""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """根据用户名获取用户"""
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()
