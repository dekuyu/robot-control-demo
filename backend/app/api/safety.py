"""
安全管理 API 路由
安全检查/安全配置/轴限位/急停
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user, get_current_admin
from app.schemas.common import ApiResponse
from app.schemas.safety import (
    SafetyCheckResult, SafetyConfigUpdate, LimitUpdate,
    SafetyConfigResponse, EmergencyStopResponse,
)
from app.services.safety import (
    run_safety_check, get_safety_config, trigger_emergency_stop,
    release_emergency_stop,
)
from app.utils.logging_utils import log_operation

router = APIRouter()


@router.get("/check", response_model=ApiResponse[SafetyCheckResult])
async def check_safety(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """执行 5 项安全检查"""
    result = await run_safety_check(db, current_user)
    return ApiResponse.success(data=SafetyCheckResult(**result))


@router.get("/config", response_model=ApiResponse[SafetyConfigResponse])
async def get_safety_config_route(db: AsyncSession = Depends(get_db)):
    """获取安全配置"""
    config = await get_safety_config(db)
    return ApiResponse.success(data=SafetyConfigResponse.model_validate(config))


@router.put("/config", response_model=ApiResponse[SafetyConfigResponse])
async def update_safety_config(
    request: SafetyConfigUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    """更新安全配置（管理员专用）"""
    config = await get_safety_config(db)
    if request.max_speed_percent is not None:
        config.max_speed_percent = request.max_speed_percent
    if request.require_confirm is not None:
        config.require_confirm = request.require_confirm
    config.updated_by = current_user.id
    await db.flush()

    await log_operation(
        db, current_user.id, current_user.username,
        "SAFETY_CONFIG_UPDATE",
        parameters={"max_speed": request.max_speed_percent},
    )
    return ApiResponse.success(data=SafetyConfigResponse.model_validate(config))


@router.put("/limits", response_model=ApiResponse[SafetyConfigResponse])
async def update_axis_limits(
    request: LimitUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    """更新轴限位（管理员专用）"""
    config = await get_safety_config(db)
    config.axis_limits = {k: v.model_dump() for k, v in request.axis_limits.items()}
    config.updated_by = current_user.id
    await db.flush()
    return ApiResponse.success(data=SafetyConfigResponse.model_validate(config))


@router.post("/emergency-stop", response_model=ApiResponse[EmergencyStopResponse])
async def emergency_stop(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    紧急停止
    不需要安全检查，直接执行
    """
    result = await trigger_emergency_stop()

    await log_operation(
        db, current_user.id, current_user.username,
        "ESTOP", target="emergency_stop",
        parameters={"trigger": "manual"},
    )
    return ApiResponse.success(data=EmergencyStopResponse(**result))
