"""
YERC 数值编解码工具
处理 YERC 协议的数值编码：物理值 ×1000 → int32 → hex → 小端对调

编码（写入方向）:
  物理值 → ×1000 → int32 → hex → 高低字节对调(小端) → 写入报文

解码（读取方向）:
  报文数据 → 小端还原 → hex → int32 → ÷1000 → 物理值
"""
import struct


def encode_value(value: float) -> bytes:
    """
    将浮点坐标/角度值编码为 YERC 协议字节格式
    步骤：
    1. 将值 ×1000 取整数（保留 3 位小数精度）
    2. 转换为 32 位有符号整数
    3. 转换为小端字节序（高低字节对调）

    示例：坐标值 123.456 mm
      123.456 × 1000 = 123456
      123456 = 0x0001E240
      小端输出: 40 E2 01 00

    Args:
        value: 原始浮点值（mm 或 度）

    Returns:
        4 字节小端编码
    """
    int_value = int(round(value * 1000))
    # '<i' 表示小端有符号 32 位整数
    return struct.pack("<i", int_value)


def decode_value(data: bytes, offset: int = 0) -> float:
    """
    将 YERC 协议字节格式解码为浮点坐标/角度值
    步骤：
    1. 读取 4 字节小端数据
    2. 转换为 32 位有符号整数
    3. 除以 1000 得到实际值

    Args:
        data: 原始字节数据
        offset: 起始偏移量

    Returns:
        解码后的浮点值（mm 或 度）
    """
    int_value = struct.unpack_from("<i", data, offset)[0]
    return int_value / 1000.0


def encode_int32(value: int) -> bytes:
    """
    将整数值编码为小端 4 字节
    用于 B 变量、IO 信号等整数值

    Args:
        value: 整数值

    Returns:
        4 字节小端编码
    """
    return struct.pack("<i", value)


def decode_int32(data: bytes, offset: int = 0) -> int:
    """
    将小端 4 字节解码为整数值

    Args:
        data: 原始字节数据
        offset: 起始偏移量

    Returns:
        解码后的整数
    """
    return struct.unpack_from("<i", data, offset)[0]


def decode_uint16(data: bytes, offset: int = 0) -> int:
    """
    将小端 2 字节解码为无符号整数

    Args:
        data: 原始字节数据
        offset: 起始偏移量

    Returns:
        解码后的无符号整数
    """
    return struct.unpack_from("<H", data, offset)[0]


def encode_uint16(value: int) -> bytes:
    """
    将无符号整数编码为小端 2 字节

    Args:
        value: 整数值 (0~65535)

    Returns:
        2 字节小端编码
    """
    return struct.pack("<H", value)


def bytes_to_hex_str(data: bytes, separator: str = " ") -> str:
    """
    将字节数组转换为人类可读的十六进制字符串
    用于日志记录和调试显示

    Args:
        data: 原始字节数据
        separator: 分隔符，默认空格

    Returns:
        十六进制字符串，如 "59 45 52 43 20 00"
    """
    return separator.join(f"{b:02X}" for b in data)


def hex_str_to_bytes(hex_str: str) -> bytes:
    """
    将十六进制字符串转换为字节数组
    支持带或不带空格分隔符的输入

    Args:
        hex_str: 十六进制字符串，如 "59 45 52 43" 或 "59455243"

    Returns:
        字节数组
    """
    # 移除所有空格
    hex_str = hex_str.replace(" ", "").replace("\n", "").replace("\r", "")
    if len(hex_str) % 2 != 0:
        raise ValueError("十六进制字符串长度必须为偶数")
    return bytes.fromhex(hex_str)


def swap_endian_16(value: int) -> int:
    """交换 16 位值的高低字节"""
    return ((value & 0xFF) << 8) | ((value >> 8) & 0xFF)
