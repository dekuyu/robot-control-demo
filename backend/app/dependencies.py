"""
FastAPI 依赖注入模块
提供数据库会话、当前用户、UDP客户端等依赖
"""
from typing import AsyncGenerator, Optional
from fastapi import Depends, HTTPException, status, WebSocket
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from app.database import get_db
from app.config import settings
from app.core.security import oauth2_scheme

# HTTP Bearer 认证方案
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):
    """
    从 JWT Token 中解析当前用户
    验证失败时返回 401 Unauthorized
    """
    from app.services.auth import get_user_by_id

    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: Optional[int] = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_id(db, int(user_id))
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被禁用",
        )
    return user


async def get_current_admin(
    current_user=Depends(get_current_user),
):
    """验证当前用户是否为管理员"""
    if current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限",
        )
    return current_user


async def get_current_engineer_or_admin(
    current_user=Depends(get_current_user),
):
    """验证当前用户是否为调试工程师或管理员（可发送UDP报文）"""
    if current_user.role.value not in ("admin", "engineer"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要调试工程师或管理员权限",
        )
    return current_user


async def ws_get_current_user(
    websocket: WebSocket,
    db: AsyncSession = Depends(get_db),
):
    """
    WebSocket 连接时的用户验证
    从 URL 参数中读取 token 并验证
    """
    from app.services.auth import get_user_by_id

    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=4001, reason="缺少认证令牌")
        return None

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: Optional[int] = payload.get("sub")
        if user_id is None:
            await websocket.close(code=4001, reason="无效的认证令牌")
            return None
    except JWTError:
        await websocket.close(code=4001, reason="无效的认证令牌")
        return None

    user = await get_user_by_id(db, int(user_id))
    if user is None or not user.is_active:
        await websocket.close(code=4001, reason="用户不存在或已禁用")
        return None
    return user
