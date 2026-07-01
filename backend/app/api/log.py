"""
操作日志 API 路由
查询/导出/统计
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.common import ApiResponse, PaginatedResponse
from app.schemas.log import LogResponse, LogStatsResponse
from app.services import log as log_service

router = APIRouter()


@router.get("", response_model=PaginatedResponse[LogResponse])
async def query_logs(
    start_time: str = Query(None),
    end_time: str = Query(None),
    operation_type: str = Query(None),
    user_id: int = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """查询操作日志（分页，普通用户只能看自己的）"""
    from app.utils.time_utils import from_iso
    st = from_iso(start_time) if start_time else None
    et = from_iso(end_time) if end_time else None

    is_admin = current_user.role.value == "admin"
    logs, total = await log_service.query_logs(
        db, st, et, operation_type, user_id,
        page, page_size, current_user.id, is_admin,
    )
    items = [LogResponse.model_validate(log) for log in logs]
    return PaginatedResponse(data=items, total=total, page=page, page_size=page_size)


@router.get("/stats", response_model=ApiResponse[LogStatsResponse])
async def get_stats(
    start_time: str = Query(None),
    end_time: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """操作日志统计"""
    from app.utils.time_utils import from_iso
    st = from_iso(start_time) if start_time else None
    et = from_iso(end_time) if end_time else None

    stats = await log_service.get_log_stats(db, st, et)
    return ApiResponse.success(data=LogStatsResponse(**stats))
