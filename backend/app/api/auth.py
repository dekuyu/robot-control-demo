"""
认证 API 路由
登录/登出/刷新Token/获取当前用户
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.common import ApiResponse
from app.schemas.user import (
    LoginRequest, LoginResponse, RefreshTokenRequest, RefreshTokenResponse, UserResponse,
)
from app.services.auth import authenticate_user, refresh_access_token
from app.core.exceptions import AppException

router = APIRouter()


@router.post("/login", response_model=ApiResponse[LoginResponse])
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    用户登录
    连续 5 次失败自动锁定 15 分钟
    """
    try:
        result = await authenticate_user(db, request.username, request.password)
        user = result["user"]
        return ApiResponse.success(
            data=LoginResponse(
                access_token=result["access_token"],
                refresh_token=result["refresh_token"],
                token_type=result["token_type"],
                user=UserResponse(
                    id=user.id,
                    username=user.username,
                    role=user.role.value,
                    is_active=user.is_active,
                    is_locked=user.is_locked,
                    last_login=user.last_login,
                    created_at=user.created_at,
                ),
            ),
            message="登录成功",
        )
    except AppException as e:
        return ApiResponse.error(code=int(e.error_code[1:]), message=e.message)


@router.post("/logout", response_model=ApiResponse)
async def logout(current_user=Depends(get_current_user)):
    """用户登出"""
    return ApiResponse.success(message="已登出")


@router.get("/me", response_model=ApiResponse[UserResponse])
async def get_current_user_info(current_user=Depends(get_current_user)):
    """获取当前登录用户信息"""
    return ApiResponse.success(
        data=UserResponse(
            id=current_user.id,
            username=current_user.username,
            role=current_user.role.value,
            is_active=current_user.is_active,
            is_locked=current_user.is_locked,
            last_login=current_user.last_login,
            created_at=current_user.created_at,
        )
    )


@router.post("/refresh", response_model=ApiResponse[RefreshTokenResponse])
async def refresh_token(request: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    """刷新 Token"""
    try:
        result = await refresh_access_token(db, request.refresh_token)
        return ApiResponse.success(
            data=RefreshTokenResponse(
                access_token=result["access_token"],
                refresh_token=result["refresh_token"],
                token_type=result["token_type"],
            ),
            message="Token 刷新成功",
        )
    except AppException as e:
        return ApiResponse.error(code=int(e.error_code[1:]), message=e.message)
