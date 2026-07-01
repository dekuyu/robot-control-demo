"""
调试终端服务
UDP 报文收发、日志记录、统计管理
"""
import time
from typing import Optional, List
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.packet_log import PacketLog
from app.services.udp_client import udp_client
from app.utils.encoding import hex_str_to_bytes, bytes_to_hex_str
from app.utils.validators import validate_hex_input
from app.core.exceptions import RobotNotConnectedError


# ===== YERC 命令模板 =====
YERC_COMMAND_TEMPLATES = [
    {
        "name": "读取机器人状态",
        "description": "0x72 - 读取运行模式、伺服状态",
        "command": "59 45 52 43 20 00 00 00 03 01 00 00 01 00 00 00 39 39 39 39 39 39 39 39 72 01 00 00",
    },
    {
        "name": "读取机器人位置",
        "description": "0x75 - 读取各轴角度与末端坐标",
        "command": "59 45 52 43 20 00 00 00 03 01 00 00 01 00 00 00 39 39 39 39 39 39 39 39 75 01 00 00",
    },
    {
        "name": "读取报警信息",
        "description": "0x70 - 读取当前报警",
        "command": "59 45 52 43 20 00 00 00 03 01 00 00 01 00 00 00 39 39 39 39 39 39 39 39 70 01 00 00",
    },
    {
        "name": "读取各轴力矩",
        "description": "0x74 - 读取各轴力矩百分比",
        "command": "59 45 52 43 20 00 00 00 03 01 00 00 01 00 00 00 39 39 39 39 39 39 39 39 74 01 00 00",
    },
    {
        "name": "读取 B 变量 B000",
        "description": "0x7A - 读取 B000 变量值",
        "command": "59 45 52 43 20 00 04 00 03 01 00 00 01 00 00 00 39 39 39 39 39 39 39 39 7A 01 00 00 00 00 00 00",
    },
    {
        "name": "读取 P 变量 P000",
        "description": "0x7F - 读取 P000 位置数据",
        "command": "59 45 52 43 20 00 04 00 03 01 00 00 01 00 00 00 39 39 39 39 39 39 39 39 7F 06 00 00 00 00 00 00",
    },
    {
        "name": "读取轴构成",
        "description": "0x73 - 读取轴配置信息",
        "command": "59 45 52 43 20 00 00 00 03 01 00 00 01 00 00 00 39 39 39 39 39 39 39 39 73 01 00 00",
    },
]


# 发送频率限制器
class RateLimiter:
    """简单的频率限制器：限制每秒最大调用次数"""

    def __init__(self, max_per_second: int = 10):
        self._max_per_second = max_per_second
        self._timestamps: List[float] = []

    def can_send(self) -> bool:
        """检查是否允许发送"""
        now = time.time()
        # 清理超过 1 秒的记录
        self._timestamps = [t for t in self._timestamps if now - t < 1.0]
        return len(self._timestamps) < self._max_per_second

    def record_send(self):
        """记录一次发送"""
        self._timestamps.append(time.time())


# 全局频率限制器
_rate_limiter = RateLimiter(max_per_second=10)


async def send_hex_data(
    hex_data: str,
    wait_response: bool = True,
    user_id: int = None,
    username: str = None,
) -> dict:
    """
    发送十六进制报文

    Args:
        hex_data: 十六进制字符串
        wait_response: 是否等待响应
        user_id: 操作者 ID
        username: 操作者用户名

    Returns:
        发送结果
    """
    if not udp_client.is_connected:
        raise RobotNotConnectedError("UDP 未连接，请先连接到机器人")

    # 频率检查
    if not _rate_limiter.can_send():
        raise ValueError("发送频率超限（最大 10 次/秒），请稍后再试")

    # 验证十六进制输入
    is_valid, error_msg = validate_hex_input(hex_data)
    if not is_valid:
        raise ValueError(error_msg)

    # 转换为字节
    data = hex_str_to_bytes(hex_data)
    data_length = len(data)

    # 记录发送
    _rate_limiter.record_send()

    response_hex = None
    response_time_ms = None

    if wait_response:
        try:
            response, elapsed = await udp_client.send_and_receive(data)
            response_hex = bytes_to_hex_str(response)
            response_time_ms = elapsed
        except Exception as e:
            # 不等待响应时，发送后直接返回
            if wait_response:
                raise
    else:
        await udp_client.send_raw(data)

    return {
        "sent_hex": hex_data.upper(),
        "response_hex": response_hex,
        "response_time_ms": response_time_ms,
        "data_length": data_length,
        "success": True,
    }


async def save_packet_log(
    db: AsyncSession,
    user_id: int,
    username: str,
    direction: str,
    target_ip: str,
    target_port: int,
    raw_hex: str,
    data_length: int,
    response_time_ms: Optional[int] = None,
):
    """保存报文日志到数据库"""
    log = PacketLog(
        user_id=user_id,
        username=username,
        direction=direction,
        target_ip=target_ip,
        target_port=target_port,
        raw_hex=raw_hex,
        data_length=data_length,
        response_time_ms=response_time_ms,
    )
    db.add(log)
    await db.flush()


async def query_packet_logs(
    db: AsyncSession,
    start_time=None,
    end_time=None,
    direction: Optional[str] = None,
    target_ip: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple:
    """查询报文日志（分页）"""
    conditions = []

    if start_time:
        conditions.append(PacketLog.timestamp >= start_time)
    if end_time:
        conditions.append(PacketLog.timestamp <= end_time)
    if direction:
        conditions.append(PacketLog.direction == direction)
    if target_ip:
        conditions.append(PacketLog.target_ip == target_ip)

    query = select(PacketLog)
    if conditions:
        query = query.where(and_(*conditions))

    count_query = select(func.count()).select_from(PacketLog)
    if conditions:
        count_query = count_query.where(and_(*conditions))
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    query = query.order_by(PacketLog.timestamp.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    logs = result.scalars().all()

    return list(logs), total


def get_templates() -> List[dict]:
    """获取 YERC 命令模板列表"""
    return YERC_COMMAND_TEMPLATES


def get_terminal_stats() -> dict:
    """获取终端统计信息"""
    return udp_client.get_stats()


def reset_terminal_stats():
    """重置终端统计"""
    udp_client.reset_stats()
