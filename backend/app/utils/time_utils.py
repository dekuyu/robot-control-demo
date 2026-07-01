"""
时间工具模块
UTC/ISO8601/本地时间转换
"""
from datetime import datetime, timezone, timedelta


def utc_now() -> datetime:
    """获取当前 UTC 时间"""
    return datetime.now(timezone.utc)


def utc_now_iso() -> str:
    """获取当前 UTC 时间的 ISO 8601 格式字符串"""
    return datetime.now(timezone.utc).isoformat()


def to_iso(dt: datetime) -> str:
    """将 datetime 对象转换为 ISO 8601 字符串"""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


def from_iso(iso_str: str) -> datetime:
    """将 ISO 8601 字符串转换为 datetime 对象"""
    dt = datetime.fromisoformat(iso_str)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def get_timestamp_ms() -> int:
    """获取当前时间戳（毫秒精度）"""
    return int(datetime.now(timezone.utc).timestamp() * 1000)
