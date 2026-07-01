"""
用户管理服务
CRUD/解锁/角色约束
"""
from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole
from app.core.security import hash_password
from app.core.exceptions import PermissionDeniedError


async def get_users(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 20,
    role: Optional[str] = None,
) -> tuple:
    """获取用户列表（分页，管理员专用）"""
    conditions = []
    if role:
        conditions.append(User.role == UserRole(role))

    query = select(User)
    if conditions:
        query = query.where(*conditions)

    # 总数
    count_query = select(func.count()).select_from(User)
    if conditions:
        count_query = count_query.where(*conditions)
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    query = query.order_by(User.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    users = result.scalars().all()

    return list(users), total


async def create_user(db: AsyncSession, username: str, password: str, role: str) -> User:
    """创建用户"""
    # 检查用户名是否已存在
    existing = await db.execute(select(User).where(User.username == username))
    if existing.scalar_one_or_none():
        raise ValueError(f"用户名 '{username}' 已存在")

    user = User(
        username=username,
        password_hash=hash_password(password),
        role=UserRole(role),
    )
    db.add(user)
    await db.flush()
    return user


async def update_user(
    db: AsyncSession, user_id: int, data: dict
) -> Optional[User]:
    """更新用户信息"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return None

    if "username" in data and data["username"]:
        user.username = data["username"]
    if "role" in data and data["role"]:
        user.role = UserRole(data["role"])
    if "is_active" in data:
        user.is_active = data["is_active"]

    await db.flush()
    return user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    """软删除用户（禁用而非物理删除）"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user:
        user.is_active = False
        await db.flush()
        return True
    return False


async def unlock_user(db: AsyncSession, user_id: int) -> bool:
    """解锁用户"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user:
        user.is_locked = False
        user.failed_login_attempts = 0
        user.locked_until = None
        await db.flush()
        return True
    return False
