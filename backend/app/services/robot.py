"""
机器人连接服务
负责连接/断开/心跳/配置管理
"""
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.robot_config import RobotConfig
from app.services.udp_client import udp_client
from app.services.yerc_protocol import yerc_protocol
from app.core.exceptions import RobotNotConnectedError, RobotConnectionTimeoutError
from app.config import settings


# 机器人运行状态缓存（内存）
_robot_status_cache = {
    "servo_on": False,
    "running_mode": "unknown",
    "alarm_active": False,
    "speed_percent": 0,
    "joints": None,
    "end_coords": None,
    "torques": [],
    "executing_program": None,
    "last_update": None,
    "emergency_stop_active": False,
}


def get_robot_status() -> dict:
    """获取当前机器人的缓存状态"""
    return _robot_status_cache.copy()


def update_robot_status(**kwargs):
    """更新机器人状态缓存"""
    _robot_status_cache.update(kwargs)
    _robot_status_cache["last_update"] = datetime.now(timezone.utc)


async def connect_to_robot(ip: str, port: int) -> bool:
    """
    连接到 YRC1000 控制柜并验证连接

    Args:
        ip: 机器人 IP
        port: 机器人端口

    Returns:
        是否连接成功

    Raises:
        RobotConnectionTimeoutError: 连接超时
    """
    try:
        # 建立 UDP 连接
        result = await udp_client.connect(robot_ip=ip, robot_port=port)
        if not result:
            raise RobotConnectionTimeoutError("UDP 连接失败")

        # 发送心跳验证连接
        try:
            # 发送读取 B000 命令作为心跳
            heartbeat_cmd = yerc_protocol.build_read_b_variable(0)
            response, _ = await udp_client.send_and_receive(heartbeat_cmd, timeout=1.0)
            update_robot_status(servo_on=False, running_mode="unknown")
            return True
        except Exception:
            # 如果无法收到响应但仍连接到了网络
            update_robot_status(servo_on=False, running_mode="unknown")
            return True
    except Exception as e:
        raise RobotConnectionTimeoutError(f"连接失败: {str(e)}")


async def disconnect_robot():
    """断开机器人连接"""
    udp_client.disconnect()
    update_robot_status(servo_on=False, running_mode="unknown", connected=False)


async def get_config_from_db(db: AsyncSession) -> Optional[RobotConfig]:
    """从数据库获取当前机器人配置"""
    result = await db.execute(
        select(RobotConfig).where(RobotConfig.is_active == True).limit(1)
    )
    return result.scalar_one_or_none()


async def save_config_to_db(
    db: AsyncSession, ip: str, port: int, name: str = "YRC1000"
) -> RobotConfig:
    """保存或更新机器人连接配置"""
    config = await get_config_from_db(db)
    if config:
        config.ip_address = ip
        config.port = port
        config.name = name
    else:
        config = RobotConfig(name=name, ip_address=ip, port=port)
        db.add(config)
    await db.flush()
    return config
