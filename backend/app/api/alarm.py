"""
报警管理 API 路由
当前报警/历史查询/复位/通知配置
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.common import ApiResponse, PaginatedResponse
from app.schemas.alarm import AlarmResponse, AlarmResetResponse
from app.services import alarm as alarm_service
from app.utils.logging_utils import log_operation
from app.core.exceptions import AppException

router = APIRouter()


@router.get("/active", response_model=ApiResponse)
async def get_active_alarms(db: AsyncSession = Depends(get_db)):
    """获取当前活跃报警"""
    alarms = await alarm_service.get_active_alarms(db)
    return ApiResponse.success(data=alarms)


@router.get("/history", response_model=PaginatedResponse)
async def get_alarm_history(
    start_time: str = Query(None),
    end_time: str = Query(None),
    level: str = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """报警历史查询（分页）"""
    from app.utils.time_utils import from_iso
    st = from_iso(start_time) if start_time else None
    et = from_iso(end_time) if end_time else None
    alarms, total = await alarm_service.get_alarm_history(db, st, et, level, page, page_size)
    return PaginatedResponse(data=alarms, total=total, page=page, page_size=page_size)


@router.post("/reset", response_model=ApiResponse[AlarmResetResponse])
async def reset_alarms(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """报警复位"""
    try:
        result = await alarm_service.reset_alarms(db, current_user.id)
        await log_operation(db, current_user.id, current_user.username, "ALARM_RESET")
        return ApiResponse.success(data=AlarmResetResponse(**result))
    except AppException as e:
        return ApiResponse.error(message=e.message)
