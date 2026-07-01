"""
机械臂控制 API 路由
伺服/程序/点动/增量/目标/直角坐标/速度
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.common import ApiResponse
from app.schemas.control import (
    ServoCommand, ProgramCommand, JogRequest, JogStopRequest,
    IncrementRequest, TargetMoveRequest, CartesianRequest, SpeedRequest,
)
from app.services import control as control_service
from app.services.safety import run_safety_check
from app.utils.logging_utils import log_operation
from app.core.exceptions import AppException

router = APIRouter()


@router.post("/servo/on", response_model=ApiResponse)
async def servo_on(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """伺服上电（需安全检查通过）"""
    try:
        # 先执行安全检查
        safety = await run_safety_check(db, current_user)
        if not safety["all_passed"]:
            return ApiResponse.error(message=f"安全检查未通过: {', '.join(safety['failures'])}")

        result = await control_service.servo_on(current_user)
        await log_operation(db, current_user.id, current_user.username, "SERVO_ON")
        return ApiResponse.success(data=result)
    except AppException as e:
        return ApiResponse.error(code=int(e.error_code[1:]), message=e.message)


@router.post("/servo/off", response_model=ApiResponse)
async def servo_off(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """伺服断电"""
    try:
        result = await control_service.servo_off(current_user)
        await log_operation(db, current_user.id, current_user.username, "SERVO_OFF")
        return ApiResponse.success(data=result)
    except AppException as e:
        return ApiResponse.error(code=int(e.error_code[1:]), message=e.message)


@router.post("/program/start", response_model=ApiResponse)
async def program_start(
    request: ProgramCommand = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """启动程序（需安全检查）"""
    try:
        safety = await run_safety_check(db, current_user)
        if not safety["all_passed"]:
            return ApiResponse.error(message=f"安全检查未通过: {', '.join(safety['failures'])}")

        program_name = request.program_name if request else None
        result = await control_service.program_start(current_user, program_name)
        await log_operation(db, current_user.id, current_user.username, "PROGRAM_START")
        return ApiResponse.success(data=result)
    except AppException as e:
        return ApiResponse.error(code=int(e.error_code[1:]), message=e.message)


@router.post("/program/stop", response_model=ApiResponse)
async def program_stop(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """停止程序"""
    try:
        result = await control_service.program_stop(current_user)
        await log_operation(db, current_user.id, current_user.username, "PROGRAM_STOP")
        return ApiResponse.success(data=result)
    except AppException as e:
        return ApiResponse.error(code=int(e.error_code[1:]), message=e.message)


@router.post("/program/pause", response_model=ApiResponse)
async def program_pause(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """暂停程序"""
    try:
        result = await control_service.program_pause(current_user)
        await log_operation(db, current_user.id, current_user.username, "PROGRAM_PAUSE")
        return ApiResponse.success(data=result)
    except AppException as e:
        return ApiResponse.error(code=int(e.error_code[1:]), message=e.message)


@router.post("/program/resume", response_model=ApiResponse)
async def program_resume(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """恢复程序"""
    try:
        result = await control_service.program_resume(current_user)
        return ApiResponse.success(data=result)
    except AppException as e:
        return ApiResponse.error(code=int(e.error_code[1:]), message=e.message)


@router.post("/alarm/reset", response_model=ApiResponse)
async def alarm_reset(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """报警复位"""
    try:
        result = await control_service.alarm_reset(current_user)
        await log_operation(db, current_user.id, current_user.username, "ALARM_RESET")
        return ApiResponse.success(data=result)
    except AppException as e:
        return ApiResponse.error(code=int(e.error_code[1:]), message=e.message)


@router.post("/jog/start", response_model=ApiResponse)
async def jog_start(
    request: JogRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """开始点动"""
    try:
        safety = await run_safety_check(db, current_user)
        if not safety["all_passed"]:
            return ApiResponse.error(message=f"安全检查未通过: {', '.join(safety['failures'])}")

        result = await control_service.jog_start(
            request.axis, request.direction, request.speed_percent, current_user
        )
        await log_operation(
            db, current_user.id, current_user.username, "JOG_START",
            target=f"axis_{request.axis}", parameters=request.model_dump(),
        )
        return ApiResponse.success(data=result)
    except AppException as e:
        return ApiResponse.error(code=int(e.error_code[1:]), message=e.message)


@router.post("/jog/stop", response_model=ApiResponse)
async def jog_stop(request: JogStopRequest, current_user=Depends(get_current_user)):
    """停止点动"""
    try:
        result = await control_service.jog_stop(request.axis)
        return ApiResponse.success(data=result)
    except AppException as e:
        return ApiResponse.error(code=int(e.error_code[1:]), message=e.message)


@router.post("/increment", response_model=ApiResponse)
async def increment_move(
    request: IncrementRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """增量移动"""
    try:
        safety = await run_safety_check(db, current_user)
        if not safety["all_passed"]:
            return ApiResponse.error(message=f"安全检查未通过: {', '.join(safety['failures'])}")

        result = await control_service.increment_move(
            request.axis, request.increment_deg, current_user
        )
        await log_operation(
            db, current_user.id, current_user.username, "INCREMENT",
            target=f"axis_{request.axis}", parameters=request.model_dump(),
        )
        return ApiResponse.success(data=result)
    except AppException as e:
        return ApiResponse.error(code=int(e.error_code[1:]), message=e.message)


@router.post("/target-move", response_model=ApiResponse)
async def target_move(
    request: TargetMoveRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """目标角度/坐标运动"""
    try:
        safety = await run_safety_check(db, current_user)
        if not safety["all_passed"]:
            return ApiResponse.error(message=f"安全检查未通过: {', '.join(safety['failures'])}")

        result = await control_service.target_move(
            request.target, request.speed_percent, request.coordinate_type, current_user
        )
        await log_operation(
            db, current_user.id, current_user.username, "TARGET_MOVE",
            parameters=request.model_dump(),
        )
        return ApiResponse.success(data=result)
    except AppException as e:
        return ApiResponse.error(code=int(e.error_code[1:]), message=e.message)


@router.post("/cartesian", response_model=ApiResponse)
async def cartesian_move(
    request: CartesianRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """直角坐标控制"""
    try:
        safety = await run_safety_check(db, current_user)
        if not safety["all_passed"]:
            return ApiResponse.error(message=f"安全检查未通过: {', '.join(safety['failures'])}")

        result = await control_service.cartesian_move(
            request.axis, request.value, request.speed_percent, current_user
        )
        await log_operation(
            db, current_user.id, current_user.username, "CARTESIAN",
            target=request.axis, parameters=request.model_dump(),
        )
        return ApiResponse.success(data=result)
    except AppException as e:
        return ApiResponse.error(code=int(e.error_code[1:]), message=e.message)


@router.put("/speed", response_model=ApiResponse)
async def set_speed(
    request: SpeedRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """设置速度"""
    try:
        result = await control_service.set_speed(request.speed_percent, current_user)
        await log_operation(
            db, current_user.id, current_user.username, "SPEED_SET",
            parameters=request.model_dump(),
        )
        return ApiResponse.success(data=result)
    except AppException as e:
        return ApiResponse.error(code=int(e.error_code[1:]), message=e.message)
