"""
变量读写服务
B/P/IO/I/D 变量读写、批量读取
"""
from typing import List, Optional
from app.services.udp_client import udp_client
from app.services.yerc_protocol import yerc_protocol
from app.utils.encoding import decode_int32, bytes_to_hex_str
from app.core.exceptions import VariableError, RobotNotConnectedError


async def read_b_variable(index: int) -> dict:
    """
    读取 B 变量（字节型变量）

    Args:
        index: B 变量编号 (0~99)

    Returns:
        {"var_type": "B", "index": 0, "value": 123, "raw_hex": "..."}
    """
    if not udp_client.is_connected:
        raise RobotNotConnectedError()

    try:
        cmd = yerc_protocol.build_read_b_variable(index)
        response, _ = await udp_client.send_and_receive(cmd)
        parsed = yerc_protocol.parse_response(response)

        if parsed["is_success"] and len(parsed["data"]) >= 4:
            value = decode_int32(parsed["data"])
            return {
                "var_type": "B",
                "index": index,
                "value": value,
                "raw_hex": bytes_to_hex_str(parsed["data"]),
            }
    except Exception as e:
        raise VariableError(f"读取 B 变量 B{index:03d} 失败: {str(e)}")

    raise VariableError(f"读取 B 变量 B{index:03d} 失败")


async def write_b_variable(index: int, value: int) -> dict:
    """
    写入 B 变量

    Args:
        index: B 变量编号
        value: 整数值

    Returns:
        {"var_type": "B", "index": 0, "value": 123}
    """
    if not udp_client.is_connected:
        raise RobotNotConnectedError()

    try:
        cmd = yerc_protocol.build_write_b_variable(index, value)
        response, _ = await udp_client.send_and_receive(cmd)
        parsed = yerc_protocol.parse_response(response)

        if parsed["is_success"]:
            return {"var_type": "B", "index": index, "value": value}
    except Exception as e:
        raise VariableError(f"写入 B 变量 B{index:03d} 失败: {str(e)}")

    raise VariableError(f"写入 B 变量 B{index:03d} 失败：机器人返回错误")


async def batch_read_b_variables(indices: List[int]) -> list:
    """
    批量读取 B 变量

    Args:
        indices: B 变量编号列表

    Returns:
        [{"var_type": "B", "index": 0, "value": 123}, ...]
    """
    results = []
    for idx in indices:
        try:
            result = await read_b_variable(idx)
            results.append(result)
        except Exception:
            results.append({"var_type": "B", "index": idx, "value": None, "error": True})
    return results


async def read_io(index: int) -> dict:
    """
    读取 IO 信号

    Args:
        index: IO 编号

    Returns:
        {"var_type": "IO", "index": 0, "value": 1, "label": "..."}
    """
    if not udp_client.is_connected:
        raise RobotNotConnectedError()

    try:
        cmd = yerc_protocol.build_read_io(index)
        response, _ = await udp_client.send_and_receive(cmd)
        parsed = yerc_protocol.parse_response(response)

        if parsed["is_success"] and len(parsed["data"]) >= 4:
            value = decode_int32(parsed["data"])
            return {
                "var_type": "IO",
                "index": index,
                "value": value,
                "label": None,
                "raw_hex": bytes_to_hex_str(parsed["data"]),
            }
    except Exception as e:
        raise VariableError(f"读取 IO {index} 失败: {str(e)}")

    raise VariableError(f"读取 IO {index} 失败")


async def write_io(index: int, value: int) -> dict:
    """
    写入 IO 信号

    Args:
        index: IO 编号
        value: 0 或 1

    Returns:
        {"var_type": "IO", "index": 0, "value": 1}
    """
    if not udp_client.is_connected:
        raise RobotNotConnectedError()

    try:
        cmd = yerc_protocol.build_write_io(index, value)
        response, _ = await udp_client.send_and_receive(cmd)
        parsed = yerc_protocol.parse_response(response)

        if parsed["is_success"]:
            return {"var_type": "IO", "index": index, "value": value}
    except Exception as e:
        raise VariableError(f"写入 IO {index} 失败: {str(e)}")

    raise VariableError(f"写入 IO {index} 失败：机器人返回错误")


async def read_d_variable(index: int) -> dict:
    """
    读取 D 变量（双精度型变量）

    Args:
        index: D 变量编号

    Returns:
        {"var_type": "D", "index": 0, "value": 0.0}
    """
    if not udp_client.is_connected:
        raise RobotNotConnectedError()

    try:
        cmd = yerc_protocol.build_read_b_variable(index)
        response, _ = await udp_client.send_and_receive(cmd)
        parsed = yerc_protocol.parse_response(response)

        if parsed["is_success"] and len(parsed["data"]) >= 4:
            value = decode_int32(parsed["data"]) / 1000.0
            return {"var_type": "D", "index": index, "value": value}
    except Exception as e:
        raise VariableError(f"读取 D 变量失败: {str(e)}")

    raise VariableError("读取 D 变量失败")


async def write_d_variable(index: int, value: float) -> dict:
    """写入 D 变量"""
    if not udp_client.is_connected:
        raise RobotNotConnectedError()

    try:
        int_value = int(round(value * 1000))
        cmd = yerc_protocol.build_write_b_variable(index, int_value)
        response, _ = await udp_client.send_and_receive(cmd)
        parsed = yerc_protocol.parse_response(response)

        if parsed["is_success"]:
            return {"var_type": "D", "index": index, "value": value}
    except Exception as e:
        raise VariableError(f"写入 D 变量失败: {str(e)}")

    raise VariableError("写入 D 变量失败")


async def read_i_variable(index: int) -> dict:
    """
    读取 I 变量（整数型变量）

    Args:
        index: I 变量编号

    Returns:
        {"var_type": "I", "index": 0, "value": 0}
    """
    if not udp_client.is_connected:
        raise RobotNotConnectedError()

    try:
        cmd = yerc_protocol.build_read_b_variable(index)
        response, _ = await udp_client.send_and_receive(cmd)
        parsed = yerc_protocol.parse_response(response)

        if parsed["is_success"] and len(parsed["data"]) >= 4:
            value = decode_int32(parsed["data"])
            return {"var_type": "I", "index": index, "value": value}
    except Exception as e:
        raise VariableError(f"读取 I 变量失败: {str(e)}")

    raise VariableError("读取 I 变量失败")
