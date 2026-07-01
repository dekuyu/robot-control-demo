"""
YERC 协议编解码模块
负责 YERC UDP 报文的构建与解析，包括数值编解码（×1000 → int32 → 小端对调）

YERC 报文结构：
  [0-3]   Magic: 59 45 52 43 ("YERC")
  [4-5]   标头大小: 20 00 (固定 32 字节，小端)
  [6-7]   数据部大小 (小端)
  [8]     命令类型: 03
  [9]     读写标识: 01(读) / 00(写)
  [10-11] 保留: 00 00
  [12-13] ACK: 01 00
  [14-15] 请求ID (小端，递增)
  [16-23] 数据块编号: "99999999"
  [24]    子标头命令编号
  [25]    数据排列编号
  [26]    单元编号
  [27]    处理标识
  [28+]   数据部 (可变长度)
"""
import struct
from typing import Optional, Tuple, List
from app.utils.encoding import encode_value, decode_value, encode_int32, decode_int32, bytes_to_hex_str


class YERCProtocol:
    """YERC 协议编解码器"""

    # 协议常量
    MAGIC = bytes([0x59, 0x45, 0x52, 0x43])  # "YERC"
    HEADER_SIZE = 32
    BLOCK_NUM = b"99999999"
    CMD_TYPE = 0x03

    def __init__(self):
        self._request_id = 0  # 递增请求 ID

    def _next_request_id(self) -> int:
        """获取下一个递增的请求 ID（循环 0~65535）"""
        self._request_id = (self._request_id + 1) % 65536
        return self._request_id

    # ===== 报文构建方法 =====

    def build_header(
        self,
        rw: int,                # 01=读取, 00=写入
        sub_cmd: int,           # 子标头命令编号 (0x72/0x75/0x7A 等)
        data_size: int = 0,     # 数据部大小
        data_arr: int = 0x01,   # 数据排列编号
        unit: int = 0x00,       # 单元编号
        process: int = 0x00,    # 处理标识
    ) -> bytes:
        """
        构建 YERC 报文的 28 字节标头

        Args:
            rw: 读写标识 0x01=读取, 0x00=写入
            sub_cmd: 子标头命令编号
            data_size: 数据部大小（字节）
            data_arr: 数据排列编号
            unit: 单元编号
            process: 处理标识

        Returns:
            28 字节标头
        """
        req_id = self._next_request_id()

        header = bytearray()
        header.extend(self.MAGIC)                           # [0-3]   Magic
        header.extend(struct.pack("<H", self.HEADER_SIZE))  # [4-5]   标头大小
        header.extend(struct.pack("<H", data_size))         # [6-7]   数据部大小
        header.append(self.CMD_TYPE)                        # [8]     命令类型
        header.append(rw)                                    # [9]     读写标识
        header.extend(b"\x00\x00")                          # [10-11] 保留
        header.extend(b"\x01\x00")                          # [12-13] ACK
        header.extend(struct.pack("<H", req_id))            # [14-15] 请求ID
        header.extend(self.BLOCK_NUM)                       # [16-23] 数据块编号
        header.append(sub_cmd)                              # [24]    子标头命令编号
        header.append(data_arr)                             # [25]    数据排列编号
        header.append(unit)                                 # [26]    单元编号
        header.append(process)                              # [27]    处理标识

        return bytes(header)

    def build_read_status(self) -> bytes:
        """构建读取机器人状态命令 (0x72)"""
        return self.build_header(rw=0x01, sub_cmd=0x72)

    def build_read_position(self) -> bytes:
        """构建读取机器人位置命令 (0x75)"""
        return self.build_header(rw=0x01, sub_cmd=0x75)

    def build_read_alarm(self) -> bytes:
        """构建读取报警信息命令 (0x70)"""
        return self.build_header(rw=0x01, sub_cmd=0x70)

    def build_read_torque(self) -> bytes:
        """构建读取各轴力矩命令 (0x74)"""
        return self.build_header(rw=0x01, sub_cmd=0x74)

    def build_read_axis_config(self) -> bytes:
        """构建读取轴构成命令 (0x73)"""
        return self.build_header(rw=0x01, sub_cmd=0x73)

    def build_read_b_variable(self, index: int) -> bytes:
        """
        构建读取 B 变量命令 (0x7A)

        Args:
            index: B 变量编号 (0~99)

        Returns:
            完整报文
        """
        data = encode_int32(index)
        header = self.build_header(rw=0x01, sub_cmd=0x7A, data_size=len(data))
        return header + data

    def build_write_b_variable(self, index: int, value: int) -> bytes:
        """
        构建写入 B 变量命令 (0x7A)

        Args:
            index: B 变量编号
            value: 要写入的整数值

        Returns:
            完整报文
        """
        data = encode_int32(index) + encode_int32(value)
        header = self.build_header(rw=0x00, sub_cmd=0x7A, data_size=len(data))
        return header + data

    def build_read_p_variable(self, index: int) -> bytes:
        """
        构建读取 P 变量命令 (0x7F)

        Args:
            index: P 变量编号 (0~127)

        Returns:
            完整报文
        """
        data = encode_int32(index)
        header = self.build_header(rw=0x01, sub_cmd=0x7F, data_size=len(data), data_arr=0x06)
        return header + data

    def build_write_p_variable_joint(self, index: int, joints: List[float]) -> bytes:
        """
        构建写入 P 变量（关节角度）命令 (0x7F)

        Args:
            index: P 变量编号
            joints: 关节角度列表 [j1, j2, ..., j7]

        Returns:
            完整报文
        """
        data = encode_int32(index)
        for j in joints:
            data += encode_value(j)
        header = self.build_header(rw=0x00, sub_cmd=0x7F, data_size=len(data), data_arr=0x06)
        return header + data

    def build_read_io(self, io_index: int) -> bytes:
        """
        构建读取 IO 信号命令 (0x76)

        Args:
            io_index: IO 编号

        Returns:
            完整报文
        """
        data = encode_int32(io_index)
        header = self.build_header(rw=0x01, sub_cmd=0x76, data_size=len(data))
        return header + data

    def build_write_io(self, io_index: int, value: int) -> bytes:
        """
        构建写入 IO 信号命令 (0x76)

        Args:
            io_index: IO 编号
            value: 0 或 1

        Returns:
            完整报文
        """
        data = encode_int32(io_index) + encode_int32(value)
        header = self.build_header(rw=0x00, sub_cmd=0x76, data_size=len(data))
        return header + data

    # ===== 报文解析方法 =====

    def parse_response(self, raw_data: bytes) -> dict:
        """
        解析 YERC 响应报文

        Args:
            raw_data: 原始响应字节

        Returns:
            解析结果字典:
            {
                "request_id": int,      # 请求 ID
                "status": int,          # 状态码 (0x80=成功)
                "is_success": bool,     # 是否成功
                "data": bytes,          # 数据部原始字节
                "hex": str              # 原始十六进制字符串
            }
        """
        if len(raw_data) < self.HEADER_SIZE:
            raise ValueError(f"响应报文太短: {len(raw_data)} 字节")

        request_id = struct.unpack_from("<H", raw_data, 14)[0]
        status = raw_data[24] if len(raw_data) > 24 else 0xFF
        data_start = self.HEADER_SIZE
        data = raw_data[data_start:] if len(raw_data) > data_start else b""

        return {
            "request_id": request_id,
            "status": status,
            "is_success": status == 0x80,
            "data": data,
            "hex": bytes_to_hex_str(raw_data),
        }

    def parse_joint_angles(self, data: bytes, num_axes: int = 7) -> List[float]:
        """
        从响应数据部解析各轴角度值
        每个轴 4 字节（int32 小端），÷1000 得到度

        Args:
            data: 数据部字节
            num_axes: 轴数量

        Returns:
            角度值列表（度），如 [45.2, -12.3, ...]
        """
        angles = []
        for i in range(min(num_axes, len(data) // 4)):
            angles.append(decode_value(data, i * 4))
        return angles

    def parse_torque_values(self, data: bytes, num_axes: int = 7) -> List[float]:
        """
        从响应数据部解析各轴力矩值
        力矩单位 N·m，×100 存储

        Args:
            data: 数据部字节
            num_axes: 轴数量

        Returns:
            力矩值列表（N·m）
        """
        torques = []
        for i in range(min(num_axes, len(data) // 4)):
            int_val = decode_int32(data, i * 4)
            torques.append(int_val / 100.0)
        return torques

    def parse_status_response(self, data: bytes) -> dict:
        """
        解析机器人状态响应 (0x72)

        返回运行模式、伺服状态等
        """
        if len(data) < 4:
            return {"mode": "unknown", "servo_on": False, "alarm_active": False}

        # 根据 YRC1000 协议响应格式解析
        # 此处为协议约定的解析逻辑，具体偏移需对照官方文档
        mode_byte = data[0] if len(data) > 0 else 0
        servo_byte = data[1] if len(data) > 1 else 0
        alarm_byte = data[2] if len(data) > 2 else 0

        # 运行模式映射
        mode_map = {
            0x00: "teaching",
            0x01: "play",
            0x02: "remote",
            0x03: "idle",
            0xFF: "error",
        }
        mode = mode_map.get(mode_byte, "unknown")

        return {
            "mode": mode,
            "servo_on": (servo_byte & 0x01) != 0,
            "alarm_active": alarm_byte != 0,
            "raw_data": bytes_to_hex_str(data),
        }


# 全局单例
yerc_protocol = YERCProtocol()
