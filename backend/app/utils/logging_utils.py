"""
操作日志记录工具
自动填充用户/时间/响应，提供统一的日志写入接口
"""
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession


async def log_operation(
    db: AsyncSession,
    user_id: int,
    username: str,
    operation_type: str,
    target: str = "",
    parameters: Optional[Dict[str, Any]] = None,
    result: str = "success",
    robot_response: Optional[str] = None,
) -> None:
    """
    向数据库写入操作日志

    Args:
        db: 数据库会话
        user_id: 操作用户 ID
        username: 操作用户名
        operation_type: 操作类型（SERVO_ON, SERVO_OFF, JOG, MOVE_TO, ESTOP, VAR_WRITE 等）
        target: 操作对象（轴号/变量名/程序名）
        parameters: 操作参数
        result: 成功/失败
        robot_response: 机器人返回的原始数据
    """
    from app.models.operation_log import OperationLog

    log_entry = OperationLog(
        user_id=user_id,
        username=username,
        operation_type=operation_type,
        target=target,
        parameters=parameters or {},
        result=result,
        robot_response=robot_response,
    )
    db.add(log_entry)
    await db.flush()


async def log_packet(
    db: AsyncSession,
    user_id: int,
    username: str,
    direction: str,
    target_ip: str,
    target_port: int,
    raw_hex: str,
    data_length: int,
    response_time_ms: Optional[int] = None,
) -> None:
    """
    向数据库写入报文日志

    Args:
        db: 数据库会话
        user_id: 操作用户 ID
        username: 操作用户名
        direction: 方向 ('send' / 'receive')
        target_ip: 目标 IP
        target_port: 目标端口
        raw_hex: 原始十六进制字符串
        data_length: 数据长度（字节）
        response_time_ms: 响应耗时（仅发送时有效）
    """
    from app.models.packet_log import PacketLog

    log_entry = PacketLog(
        user_id=user_id,
        username=username,
        direction=direction,
        target_ip=target_ip,
        target_port=target_port,
        raw_hex=raw_hex,
        data_length=data_length,
        response_time_ms=response_time_ms,
    )
    db.add(log_entry)
    await db.flush()
