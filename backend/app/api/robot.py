"""
机器人连接 API 路由
连接/断开/状态/配置/心跳
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.common import ApiResponse
from app.schemas.robot import (
    RobotConfigCreate, RobotConfigResponse, RobotConnectRequest,
    RobotStatusResponse, HeartbeatResponse, JointAngles, EndCoords,
)
from app.services.robot import (
    connect_to_robot, disconnect_robot, get_robot_status,
    get_config_from_db, save_config_to_db,
)
from app.services.udp_client import udp_client
from app.core.exceptions import AppException

router = APIRouter()


@router.post("/connect", response_model=ApiResponse)
async def connect_robot(
    request: RobotConnectRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """连接到 YRC1000 控制柜"""
    try:
        await connect_to_robot(request.ip, request.port)
        config = await save_config_to_db(db, request.ip, request.port)
        return ApiResponse.success(
            data={"connected": True, "config_id": config.id},
            message=f"已连接到 {request.ip}:{request.port}",
        )
    except AppException as e:
        return ApiResponse.error(code=int(e.error_code[1:]), message=e.message)


@router.post("/disconnect", response_model=ApiResponse)
async def disconnect_robot_route(current_user=Depends(get_current_user)):
    """断开机器人连接"""
    await disconnect_robot()
    return ApiResponse.success(data={"connected": False}, message="已断开连接")


@router.get("/status", response_model=ApiResponse[RobotStatusResponse])
async def get_robot_status_route():
    """获取机器人完整状态"""
    status = get_robot_status()
    joints = status.get("joints", {})
    end_coords = status.get("end_coords", {})

    data = RobotStatusResponse(
        connected=udp_client.is_connected,
        servo_on=status.get("servo_on", False),
        running_mode=status.get("running_mode", "unknown"),
        alarm_active=status.get("alarm_active", False),
        speed_percent=status.get("speed_percent", 0),
        joints=JointAngles(**joints) if joints else None,
        end_coords=EndCoords(**end_coords) if end_coords else None,
        torques=status.get("torques"),
        executing_program=status.get("executing_program"),
        last_heartbeat=status.get("last_update"),
    )
    return ApiResponse.success(data=data)


@router.get("/config", response_model=ApiResponse[RobotConfigResponse])
async def get_config(db: AsyncSession = Depends(get_db)):
    """获取当前机器人连接配置"""
    config = await get_config_from_db(db)
    if config:
        return ApiResponse.success(data=RobotConfigResponse.model_validate(config))
    return ApiResponse.error(message="未找到配置")


@router.put("/config", response_model=ApiResponse[RobotConfigResponse])
async def update_config(
    request: RobotConfigCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """更新连接配置"""
    config = await save_config_to_db(db, request.ip, request.port, request.name)
    return ApiResponse.success(data=RobotConfigResponse.model_validate(config))


@router.get("/heartbeat", response_model=ApiResponse[HeartbeatResponse])
async def heartbeat():
    """心跳状态查询"""
    status = get_robot_status()
    return ApiResponse.success(
        data=HeartbeatResponse(
            alive=udp_client.is_connected,
            last_beat=status.get("last_update"),
        )
    )
