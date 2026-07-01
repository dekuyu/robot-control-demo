"""
用户管理 API 路由（管理员专用）
用户 CRUD / 解锁
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_admin
from app.schemas.common import ApiResponse, PaginatedResponse
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services import user as user_service

router = APIRouter()


@router.get("", response_model=PaginatedResponse[UserResponse])
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    role: str = Query(None),
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """用户列表（管理员专用）"""
    users, total = await user_service.get_users(db, page, page_size, role)
    items = [UserResponse.model_validate(u) for u in users]
    return PaginatedResponse(data=items, total=total, page=page, page_size=page_size)


@router.post("", response_model=ApiResponse[UserResponse])
async def create_user(
    request: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """创建用户"""
    try:
        user = await user_service.create_user(db, request.username, request.password, request.role)
        return ApiResponse.success(data=UserResponse.model_validate(user))
    except ValueError as e:
        return ApiResponse.error(message=str(e))


@router.put("/{user_id}", response_model=ApiResponse[UserResponse])
async def update_user(
    user_id: int, request: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """更新用户"""
    user = await user_service.update_user(db, user_id, request.model_dump(exclude_none=True))
    if not user:
        return ApiResponse.error(message="用户不存在")
    return ApiResponse.success(data=UserResponse.model_validate(user))


@router.delete("/{user_id}", response_model=ApiResponse)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """软删除用户"""
    ok = await user_service.delete_user(db, user_id)
    return ApiResponse.success(message="已禁用" if ok else "用户不存在")


@router.post("/{user_id}/unlock", response_model=ApiResponse)
async def unlock_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    """解锁用户"""
    ok = await user_service.unlock_user(db, user_id)
    return ApiResponse.success(message="已解锁" if ok else "用户不存在")
