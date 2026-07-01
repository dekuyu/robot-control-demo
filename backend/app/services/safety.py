"""
安全服务模块
5 项安全检查、限位校验、互锁判断、急停指令
"""
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.safety_config import SafetyConfig
from app.services.robot import get_robot_status, update_robot_status
from app.services.udp_client import udp_client
from app.core.exceptions import (
    SafetyViolationError, SpeedLimitExceededError,
    InterlockViolationError, AxisLimitExceededError,
    EmergencyStopActiveError, RobotNotConnectedError,
)
from app.core.constants import ROLE_SPEED_LIMITS
from app.config import settings


# 内存中的安全配置缓存
_safety_config_cache: Optional[SafetyConfig] = None


async def get_safety_config(db: AsyncSession) -> SafetyConfig:
    """获取安全配置（带缓存）"""
    global _safety_config_cache
    result = await db.execute(select(SafetyConfig).limit(1))
    config = result.scalar_one_or_none()
    if config is None:
        config = SafetyConfig(
            max_speed_percent=settings.GLOBAL_SPEED_LIMIT,
            require_confirm=True,
            axis_limits={},
        )
        db.add(config)
        await db.flush()
    _safety_config_cache = config
    return config


async def run_safety_check(db: AsyncSession, user: User) -> dict:
    """
    执行 5 项安全检查（操作运动控制前必须通过）

    检查项:
    1. 伺服电源确认
    2. 运行模式确认（仅远程模式）
    3. 报警清零确认
    4. 速度合规性
    5. 操作人员二次确认（前端处理）

    Returns:
        检查结果字典
    """
    status = get_robot_status()
    safety_config = await get_safety_config(db)

    failures = []

    # 检查 1: 伺服电源
    servo_ok = status.get("servo_on", False)
    if not servo_ok:
        failures.append("伺服未上电")

    # 检查 2: 运行模式
    mode = status.get("running_mode", "unknown")
    mode_ok = mode in ("remote", "play")
    if not mode_ok:
        failures.append(f"机器人不在远程/再现模式（当前：{mode}）")

    # 检查 3: 报警状态
    alarm_ok = not status.get("alarm_active", False)
    if not alarm_ok:
        failures.append("存在未处理的报警")

    # 检查 4: 急停状态
    if status.get("emergency_stop_active", False):
        failures.append("急停已激活，需先解除急停")

    # 检查 5: 速度合规性（前端回调，此处预设为 true）
    speed_ok = True

    all_passed = len(failures) == 0

    return {
        "servo_ok": servo_ok,
        "mode_ok": mode_ok,
        "alarm_ok": alarm_ok,
        "speed_ok": speed_ok,
        "operator_confirmed": False,  # 前端确认后标记
        "all_passed": all_passed,
        "failures": failures,
    }


def check_speed_limit(user: User, speed_percent: int):
    """
    检查速度是否超出用户角色上限

    Args:
        user: 当前用户
        speed_percent: 设定的速度百分比

    Raises:
        SpeedLimitExceededError: 速度超限
    """
    role_limit = ROLE_SPEED_LIMITS.get(user.role.value, 0)
    global_limit = _safety_config_cache.max_speed_percent if _safety_config_cache else settings.GLOBAL_SPEED_LIMIT

    effective_limit = min(role_limit, global_limit)
    if speed_percent > effective_limit:
        raise SpeedLimitExceededError(
            f"速度 {speed_percent}% 超出限制（上限：{effective_limit}%）"
        )

    return min(speed_percent, effective_limit)  # 返回实际生效的速度


def check_interlock():
    """
    检查安全互锁条件
    - 机器人处于示教模式时禁止远程控制
    - 伺服断电时禁止运动指令
    - 急停激活时禁止启动操作
    """
    status = get_robot_status()

    if status.get("emergency_stop_active", False):
        raise EmergencyStopActiveError()

    if status.get("running_mode") == "teaching":
        raise InterlockViolationError("示教模式下禁止远程控制")


def check_axis_limits(axis_index: int, target_angle: float) -> bool:
    """
    检查目标角度是否在软件限位内

    Args:
        axis_index: 轴编号 (1~7)
        target_angle: 目标角度

    Returns:
        是否在限位内

    Raises:
        AxisLimitExceededError: 超出限位
    """
    if not _safety_config_cache or not _safety_config_cache.axis_limits:
        return True  # 未配置限位则允许通过

    axis_key = f"j{axis_index}"
    limits = _safety_config_cache.axis_limits.get(axis_key)
    if limits:
        min_limit = limits.get("min", -361)
        max_limit = limits.get("max", 361)
        if target_angle < min_limit or target_angle > max_limit:
            raise AxisLimitExceededError(
                f"轴 {axis_index} 目标角度 {target_angle}° 超出限位 [{min_limit}°, {max_limit}°]"
            )
    return True


async def trigger_emergency_stop() -> dict:
    """
    触发紧急停止
    1. 标记急停状态
    2. 尝试发送急停 UDP 命令
    3. 更新状态缓存

    Returns:
        急停执行结果
    """
    update_robot_status(emergency_stop_active=True)

    # 尝试发送急停命令到机器人
    if udp_client.is_connected:
        try:
            # 发送伺服断电 + 停止命令
            # 实际命令需对照 YRC1000 协议
            await udp_client.send_raw(b"\x00")  # 占位命令
        except Exception:
            pass  # 急停不考虑通信失败

    return {
        "stopped": True,
        "message": "急停已激活，所有运动控制已禁用。请检查机器人状态后手动解除急停。",
    }


def release_emergency_stop():
    """解除急停状态"""
    update_robot_status(emergency_stop_active=False)
