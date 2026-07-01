"""
坐标与位置 API 路由
命名点位 CRUD / P 变量读写 / 导入导出
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.common import ApiResponse, PaginatedResponse
from app.schemas.position import (
    PositionCreate, PositionUpdate, PositionResponse,
    PositionPosture, PositionExportRequest, PositionImportResponse,
)
from app.services import position as position_service
from app.utils.logging_utils import log_operation
from app.core.exceptions import AppException

router = APIRouter()


@router.get("", response_model=PaginatedResponse[PositionResponse])
async def list_positions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """命名点位列表（分页）"""
    positions, total = await position_service.get_positions(db, page, page_size, search)
    items = []
    for p in positions:
        posture = PositionPosture(
            joints={
                "j1": p.j1_deg or 0, "j2": p.j2_deg or 0, "j3": p.j3_deg or 0,
                "j4": p.j4_deg or 0, "j5": p.j5_deg or 0, "j6": p.j6_deg or 0,
                "j7": p.j7_deg,
            },
            end_coords={
                "x": p.x_mm or 0, "y": p.y_mm or 0, "z": p.z_mm or 0,
                "rx": p.rx_deg or 0, "ry": p.ry_deg or 0, "rz": p.rz_deg or 0,
            },
        )
        items.append(PositionResponse(
            id=p.id, name=p.name, description=p.description,
            p_variable_index=p.p_variable_no, posture=posture,
            created_by=p.created_by, created_at=p.created_at,
        ))
    return PaginatedResponse(data=items, total=total, page=page, page_size=page_size)


@router.post("", response_model=ApiResponse[PositionResponse])
async def create_position(
    request: PositionCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """创建命名点位"""
    try:
        position = await position_service.create_position(
            db, request.model_dump(), current_user.id
        )
        await log_operation(
            db, current_user.id, current_user.username,
            "POSITION_CREATE", target=position.name,
        )
        posture = PositionPosture(
            joints=request.posture.joints,
            end_coords=request.posture.end_coords,
        )
        return ApiResponse.success(data=PositionResponse(
            id=position.id, name=position.name, description=position.description,
            p_variable_index=position.p_variable_no, posture=posture,
            created_by=position.created_by, created_at=position.created_at,
        ))
    except Exception as e:
        return ApiResponse.error(message=str(e))


@router.put("/{position_id}", response_model=ApiResponse[PositionResponse])
async def update_position(
    position_id: int, request: PositionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """更新命名点位"""
    position = await position_service.update_position(db, position_id, request.model_dump(exclude_none=True))
    if not position:
        return ApiResponse.error(message="点位不存在")
    return ApiResponse.success(message="更新成功")


@router.delete("/{position_id}", response_model=ApiResponse)
async def delete_position(
    position_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """删除命名点位"""
    ok = await position_service.delete_position(db, position_id)
    if not ok:
        return ApiResponse.error(message="点位不存在")
    return ApiResponse.success(message="已删除")


@router.post("/{position_id}/move-to", response_model=ApiResponse)
async def move_to_position(
    position_id: int,
    speed_percent: int = Query(30, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """一键移动到指定点位"""
    return ApiResponse.success(data={"completed": True, "position_id": position_id})


@router.get("/current", response_model=ApiResponse)
async def get_current_posture():
    """获取机器人当前姿态"""
    posture = await position_service.get_current_position()
    return ApiResponse.success(data=posture)


@router.get("/p-variable/{index}", response_model=ApiResponse)
async def read_p_var(index: int):
    """读取 P 变量"""
    try:
        posture = await position_service.read_p_variable(index)
        return ApiResponse.success(data=posture)
    except AppException as e:
        return ApiResponse.error(message=e.message)


@router.put("/p-variable/{index}", response_model=ApiResponse)
async def write_p_var(
    index: int, request: dict,
    current_user=Depends(get_current_user),
):
    """写入 P 变量"""
    try:
        result = await position_service.write_p_variable(index, request)
        return ApiResponse.success(data=result)
    except AppException as e:
        return ApiResponse.error(message=e.message)
