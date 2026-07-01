"""
后台轮询任务模块
FastAPI lifespan 中启动/停止的后台 asyncio 任务
"""
import asyncio
from typing import Optional

from app.services.udp_client import udp_client
from app.services.yerc_protocol import yerc_protocol
from app.services.ws_manager import ws_manager
from app.services.robot import update_robot_status
from app.schemas.ws import WSMessage, WSMessageType
from app.utils.time_utils import utc_now_iso
from app.config import settings

# 后台任务引用，用于生命周期管理
_background_tasks: list = []


async def poll_robot_status():
    """
    状态轮询任务（每 20ms）
    读取机器人核心状态并通过 WebSocket 推送
    """
    while udp_client.is_connected:
        try:
            # 发送读取状态命令 (0x72)
            cmd = yerc_protocol.build_read_status()
            response, _ = await udp_client.send_and_receive(cmd)
            parsed = yerc_protocol.parse_response(response)

            if parsed["is_success"]:
                status_data = yerc_protocol.parse_status_response(parsed["data"])
                update_robot_status(
                    servo_on=status_data.get("servo_on", False),
                    running_mode=status_data.get("mode", "unknown"),
                    alarm_active=status_data.get("alarm_active", False),
                )

                # WebSocket 推送状态
                await ws_manager.broadcast(WSMessage(
                    type=WSMessageType.ROBOT_STATUS,
                    timestamp=utc_now_iso(),
                    data={
                        "servo_on": status_data.get("servo_on", False),
                        "running_mode": status_data.get("mode", "unknown"),
                        "alarm_active": status_data.get("alarm_active", False),
                        "speed_percent": 0,
                    },
                ))

            await asyncio.sleep(settings.STATUS_POLL_INTERVAL)
        except Exception:
            await asyncio.sleep(0.05)  # 出错时等待 50ms 再重试


async def poll_robot_position():
    """
    位置轮询任务（每 20ms）
    读取关节角度和末端坐标并通过 WebSocket 推送
    """
    while udp_client.is_connected:
        try:
            cmd = yerc_protocol.build_read_position()
            response, _ = await udp_client.send_and_receive(cmd)
            parsed = yerc_protocol.parse_response(response)

            if parsed["is_success"]:
                angles = yerc_protocol.parse_joint_angles(parsed["data"])

                positions = {
                    "j1": angles[0] if len(angles) > 0 else 0,
                    "j2": angles[1] if len(angles) > 1 else 0,
                    "j3": angles[2] if len(angles) > 2 else 0,
                    "j4": angles[3] if len(angles) > 3 else 0,
                    "j5": angles[4] if len(angles) > 4 else 0,
                    "j6": angles[5] if len(angles) > 5 else 0,
                    "j7": angles[6] if len(angles) > 6 else 0,
                }

                await ws_manager.broadcast(WSMessage(
                    type=WSMessageType.ROBOT_POSITION,
                    timestamp=utc_now_iso(),
                    data={
                        "joints": positions,
                        "end_coords": {"x": 0, "y": 0, "z": 0, "rx": 0, "ry": 0, "rz": 0},
                    },
                ))

            await asyncio.sleep(settings.STATUS_POLL_INTERVAL)
        except Exception:
            await asyncio.sleep(0.05)


async def poll_robot_torque():
    """
    力矩轮询任务（每 50ms）
    读取各轴力矩并通过 WebSocket 推送
    """
    while udp_client.is_connected:
        try:
            cmd = yerc_protocol.build_read_torque()
            response, _ = await udp_client.send_and_receive(cmd)
            parsed = yerc_protocol.parse_response(response)

            if parsed["is_success"]:
                torques = yerc_protocol.parse_torque_values(parsed["data"])
                await ws_manager.broadcast(WSMessage(
                    type=WSMessageType.ROBOT_TORQUE,
                    timestamp=utc_now_iso(),
                    data={"torques": torques},
                ))

            await asyncio.sleep(settings.TORQUE_POLL_INTERVAL)
        except Exception:
            await asyncio.sleep(0.05)


async def poll_alarm():
    """
    报警轮询任务
    有变化时立即推送
    """
    last_alarm_state = False
    while udp_client.is_connected:
        try:
            cmd = yerc_protocol.build_read_alarm()
            response, _ = await udp_client.send_and_receive(cmd)
            parsed = yerc_protocol.parse_response(response)

            has_alarm = not parsed["is_success"] or (parsed["data"] and len(parsed["data"]) > 0)
            if has_alarm != last_alarm_state:
                last_alarm_state = has_alarm
                await ws_manager.broadcast(WSMessage(
                    type=WSMessageType.ALARM_UPDATE,
                    timestamp=utc_now_iso(),
                    data={"has_active_alarm": has_alarm, "alarms": []},
                ))

            await asyncio.sleep(0.1)  # 报警轮询 100ms
        except Exception:
            await asyncio.sleep(0.1)


async def heartbeat_monitor():
    """
    心跳监控任务（每 1 秒）
    通过读取 B000 变量验证连接状态
    """
    fail_count = 0
    max_fails = 5

    while udp_client.is_connected:
        try:
            cmd = yerc_protocol.build_read_b_variable(0)
            response, _ = await udp_client.send_and_receive(cmd, timeout=0.5)
            fail_count = 0  # 成功则重置

            await ws_manager.broadcast(WSMessage(
                type=WSMessageType.CONNECTION_UPDATE,
                timestamp=utc_now_iso(),
                data={"connected": True, "last_heartbeat": utc_now_iso()},
            ))
        except Exception:
            fail_count += 1
            if fail_count >= max_fails:
                await ws_manager.broadcast(WSMessage(
                    type=WSMessageType.CONNECTION_UPDATE,
                    timestamp=utc_now_iso(),
                    data={"connected": False, "last_heartbeat": utc_now_iso()},
                ))

        await asyncio.sleep(1.0)


async def start_background_tasks():
    """启动所有后台轮询任务"""
    global _background_tasks
    tasks = [
        poll_robot_status(),
        poll_robot_position(),
        poll_robot_torque(),
        poll_alarm(),
        heartbeat_monitor(),
    ]
    _background_tasks = [asyncio.create_task(t) for t in tasks]


async def stop_background_tasks():
    """停止所有后台轮询任务"""
    for task in _background_tasks:
        task.cancel()
    _background_tasks.clear()
