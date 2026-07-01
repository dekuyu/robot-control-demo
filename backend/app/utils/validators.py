"""
输入校验工具
IP格式、角度范围、速度范围、变量索引校验
"""
import re
from ipaddress import ip_address


def is_valid_ip(ip: str) -> bool:
    """验证是否为有效的 IPv4 地址"""
    try:
        ip_address(ip)
        return True
    except ValueError:
        return False


def is_valid_port(port: int) -> bool:
    """验证端口号范围（1~65535，0 表示任意端口）"""
    return 0 <= port <= 65535


def is_valid_angle(angle: float, axis_index: int = None) -> bool:
    """
    验证角度值是否在合理范围内
    各轴关节角度通常 -360° ~ 360°
    """
    return -360.0 <= angle <= 360.0


def is_valid_speed(speed: int) -> bool:
    """验证速度百分比范围（0~100）"""
    return 0 <= speed <= 100


def is_valid_b_variable_index(index: int) -> bool:
    """验证 B 变量编号（0~99）"""
    return 0 <= index <= 99


def is_valid_p_variable_index(index: int) -> bool:
    """验证 P 变量编号（0~127）"""
    return 0 <= index <= 127


def is_valid_axis_index(index: int) -> bool:
    """验证轴编号（1~7）"""
    return 1 <= index <= 7


def sanitize_hex_input(hex_str: str) -> str:
    """
    清理十六进制输入，移除非法字符
    保留 0-9, a-f, A-F, 空格, 换行, 回车
    """
    # 移除所有非十六进制字符（保留空格）
    hex_str = re.sub(r"[^0-9a-fA-F\s\r\n]", "", hex_str)
    return hex_str


def validate_hex_input(hex_str: str) -> tuple[bool, str]:
    """
    验证十六进制输入是否合法
    返回 (是否合法, 错误消息)
    """
    hex_str = hex_str.replace(" ", "").replace("\n", "").replace("\r", "")
    if len(hex_str) == 0:
        return False, "输入不能为空"
    if len(hex_str) % 2 != 0:
        return False, "十六进制字符串长度必须为偶数"
    try:
        bytes.fromhex(hex_str)
        return True, ""
    except ValueError:
        return False, "包含无效的十六进制字符"
