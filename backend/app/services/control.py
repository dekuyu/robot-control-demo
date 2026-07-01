"""
机械臂控制服务
伺服上电/断电、程序启停暂停复位、报警复位、
点动(JOG)/增量(Increment)/目标移动(Target)/直角坐标(Cartesian)/速度设置
"""
import asyncio
from typing import Optional

from app.services.udp_client import udp_client
from app.services.yerc_protocol import yerc_protocol
from app.services.robot import update_robot_status, get_robot_status
from app.services.safety import (
    check_interlock, check_speed_limit, check_axis_limits,
)
from app.core.exceptions import (
    RobotNotConnectedError, ServoOperationError, ControlCommandError,
)
from app.models.user import User


async def servo_on(user: User) -> dict:
    """
    伺服上电
    通过 B 变量或专用命令触发伺服使能

    前置条件：安全模式为远程/再现模式
    """
    check_interlock()
    if not udp_client.is_connected:
        raise RobotNotConnectedError()

    try:
        # 通过 B 变量触发伺服上电（B000 = 1 或其他约定值）
        cmd = yerc_protocol.build_write_b_variable(0, 1)
        await udp_client.send_and_receive(cmd)
        update_robot_status(servo_on=True)
        return {"servo_on": True, "message": "伺服已上电"}
    except Exception as e:
        raise ServoOperationError(f"伺服上电失败: {str(e)}")


async def servo_off(user: User) -> dict:
    """伺服断电（停止类别 2）"""
    if not udp_client.is_connected:
        raise RobotNotConnectedError()

    try:
        cmd = yerc_protocol.build_write_b_variable(0, 0)
        await udp_client.send_and_receive(cmd)
        update_robot_status(servo_on=False)
        return {"servo_on": False, "message": "伺服已断电"}
    except Exception as e:
        raise ServoOperationError(f"伺服断电失败: {str(e)}")


async def program_start(user: User, program_name: Optional[str] = None) -> dict:
    """启动程序"""
    check_interlock()
    if not udp_client.is_connected:
        raise RobotNotConnectedError()

    try:
        # 通过 B 变量触发程序启动
        cmd = yerc_protocol.build_write_b_variable(1, 1)
        await udp_client.send_and_receive(cmd)
        return {"running": True, "program": program_name or "default"}
    except Exception as e:
        raise ControlCommandError(f"程序启动失败: {str(e)}")


async def program_stop(user: User) -> dict:
    """停止程序（停止类别 1）"""
    if not udp_client.is_connected:
        raise RobotNotConnectedError()

    try:
        cmd = yerc_protocol.build_write_b_variable(1, 0)
        await udp_client.send_and_receive(cmd)
        return {"running": False, "message": "程序已停止"}
    except Exception as e:
        raise ControlCommandError(f"程序停止失败: {str(e)}")


async def program_pause(user: User) -> dict:
    """暂停程序"""
    if not udp_client.is_connected:
        raise RobotNotConnectedError()

    try:
        cmd = yerc_protocol.build_write_b_variable(2, 1)
        await udp_client.send_and_receive(cmd)
        return {"paused": True, "message": "程序已暂停"}
    except Exception as e:
        raise ControlCommandError(f"程序暂停失败: {str(e)}")


async def program_resume(user: User) -> dict:
    """恢复程序"""
    check_interlock()
    if not udp_client.is_connected:
        raise RobotNotConnectedError()

    try:
        cmd = yerc_protocol.build_write_b_variable(2, 0)
        await udp_client.send_and_receive(cmd)
        return {"paused": False, "message": "程序已恢复"}
    except Exception as e:
        raise ControlCommandError(f"程序恢复失败: {str(e)}")


async def alarm_reset(user: User) -> dict:
    """报警复位"""
    if not udp_client.is_connected:
        raise RobotNotConnectedError()

    try:
        cmd = yerc_protocol.build_write_b_variable(3, 1)
        await udp_client.send_and_receive(cmd)
        update_robot_status(alarm_active=False)
        return {"reset": True, "message": "报警已复位"}
    except Exception as e:
        raise ControlCommandError(f"报警复位失败: {str(e)}")


async def jog_start(
    axis: int, direction: str, speed_percent: int, user: User
) -> dict:
    """
    开始点动控制（JOG）
    按住方向按钮持续运动，松开立即停止

    Args:
        axis: 轴编号 1~7
        direction: 'positive' / 'negative'
        speed_percent: 速度百分比
    """
    check_interlock()
    check_speed_limit(user, speed_percent)
    check_axis_limits(axis, float("inf" if direction == "positive" else "-inf"))

    # 点动增量角度：1°
    increment_deg = 1.0 if direction == "positive" else -1.0

    try:
        # 通过 P 变量 + B 变量实现点动
        # 实际实现需根据 YRC1000 协议调整
        cmd = yerc_protocol.build_write_b_variable(10 + axis, 1)
        await udp_client.send_raw(cmd)
        return {"moving": True, "axis": axis, "direction": direction}
    except Exception as e:
        raise ControlCommandError(f"点动失败: {str(e)}")


async def jog_stop(axis: int) -> dict:
    """停止点动"""
    try:
        cmd = yerc_protocol.build_write_b_variable(10 + axis, 0)
        await udp_client.send_raw(cmd)
        return {"moving": False, "axis": axis}
    except Exception as e:
        raise ControlCommandError(f"停止点动失败: {str(e)}")


async def increment_move(axis: int, increment_deg: float, user: User) -> dict:
    """
    增量移动
    输入步长值，点击执行精确移动

    Args:
        axis: 轴编号
        increment_deg: 增量角度
    """
    check_interlock()
    check_axis_limits(axis, increment_deg)

    if not udp_client.is_connected:
        raise RobotNotConnectedError()

    try:
        # 通过 P 变量存储增量目标
        cmd = yerc_protocol.build_write_b_variable(20 + axis, 1)
        await udp_client.send_and_receive(cmd)
        return {"completed": True, "axis": axis, "increment": increment_deg}
    except Exception as e:
        raise ControlCommandError(f"增量移动失败: {str(e)}")


async def target_move(target: dict, speed_percent: int, coordinate_type: str, user: User) -> dict:
    """
    目标角度/坐标运动
    直接输入目标值，一键移动到指定位置

    Args:
        target: 目标位置字典
        speed_percent: 速度百分比
        coordinate_type: 'joint' 或 'cartesian'
    """
    check_interlock()
    check_speed_limit(user, speed_percent)

    # 检查各轴限位
    if coordinate_type == "joint":
        for key, value in target.items():
            if key.startswith("j"):
                axis_num = int(key[1:])
                check_axis_limits(axis_num, float(value))

    if not udp_client.is_connected:
        raise RobotNotConnectedError()

    try:
        cmd = yerc_protocol.build_write_b_variable(30, 1)
        await udp_client.send_and_receive(cmd)
        return {"completed": True, "target": target}
    except Exception as e:
        raise ControlCommandError(f"目标运动失败: {str(e)}")


async def cartesian_move(
    axis: str, value: float, speed_percent: int, user: User
) -> dict:
    """
    直角坐标系控制
    在笛卡尔坐标系下控制末端位置

    Args:
        axis: 'x'/'y'/'z'/'rx'/'ry'/'rz'
        value: 移动值
        speed_percent: 速度百分比
    """
    check_interlock()
    check_speed_limit(user, speed_percent)

    if not udp_client.is_connected:
        raise RobotNotConnectedError()

    try:
        cmd = yerc_protocol.build_write_b_variable(40, 1)
        await udp_client.send_and_receive(cmd)
        return {"completed": True, "axis": axis, "value": value}
    except Exception as e:
        raise ControlCommandError(f"直角坐标控制失败: {str(e)}")


async def set_speed(speed_percent: int, user: User) -> dict:
    """
    设置全局速度

    Args:
        speed_percent: 速度百分比 0~100
    """
    actual_speed = check_speed_limit(user, speed_percent)
    update_robot_status(speed_percent=actual_speed)

    return {
        "speed_percent": speed_percent,
        "actual_speed": actual_speed,
        "message": f"速度已设置为 {speed_percent}%（实际生效：{actual_speed}%）",
    }
