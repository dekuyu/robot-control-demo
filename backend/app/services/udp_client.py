"""
UDP 通信客户端模块
基于 asyncio.DatagramProtocol 实现 YERC 协议 UDP 通信
提供请求/响应管理、超时重试机制
"""
import asyncio
import time
from typing import Optional, Tuple, Callable
from app.config import settings
from app.utils.encoding import bytes_to_hex_str


class UDPClient:
    """
    YRC1000 UDP 通信客户端
    管理 UDP Socket、请求-响应匹配、心跳检测
    """

    def __init__(self):
        self._transport: Optional[asyncio.DatagramTransport] = None
        self._protocol: Optional["_YERCUDPProtocol"] = None
        self._is_connected = False
        self._robot_ip: str = settings.ROBOT_DEFAULT_IP
        self._robot_port: int = settings.ROBOT_DEFAULT_PORT
        self._local_port: int = settings.ROBOT_LOCAL_PORT
        self._pending_requests: dict = {}  # req_id -> asyncio.Future
        self._on_data_received: Optional[Callable] = None  # 数据接收回调

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    @property
    def robot_ip(self) -> str:
        return self._robot_ip

    @property
    def robot_port(self) -> int:
        return self._robot_port

    async def connect(
        self,
        robot_ip: str,
        robot_port: int = 10040,
        local_port: int = 0,
    ) -> bool:
        """
        连接到 YRC1000 控制柜

        Args:
            robot_ip: 机器人 IP 地址
            robot_port: 机器人 UDP 端口
            local_port: 本地端口（0 = 任意端口）

        Returns:
            是否连接成功
        """
        self._robot_ip = robot_ip
        self._robot_port = robot_port
        self._local_port = local_port
        self._pending_requests.clear()

        loop = asyncio.get_event_loop()

        # 创建 UDP 端点
        try:
            transport, protocol = await loop.create_datagram_endpoint(
                lambda: _YERCUDPProtocol(self),
                local_addr=("0.0.0.0", local_port),
                remote_addr=(robot_ip, robot_port),
            )
            self._transport = transport
            self._protocol = protocol
            self._is_connected = True
            return True
        except Exception as e:
            self._is_connected = False
            raise ConnectionError(f"UDP 连接失败: {e}")

    def disconnect(self):
        """断开 UDP 连接"""
        if self._transport:
            self._transport.close()
            self._transport = None
        self._protocol = None
        self._is_connected = False
        self._pending_requests.clear()

    async def send_and_receive(
        self,
        data: bytes,
        timeout: float = None,
        retries: int = None,
    ) -> Tuple[bytes, float]:
        """
        发送 UDP 数据并等待响应（带超时重试机制）

        Args:
            data: 要发送的字节数据
            timeout: 超时时间（秒），默认从配置加载
            retries: 最大重试次数，默认从配置加载

        Returns:
            (响应数据, 响应耗时毫秒)

        Raises:
            ConnectionError: 未连接或连接超时
        """
        if not self._is_connected:
            raise ConnectionError("UDP 未连接")

        timeout = timeout or settings.UDP_TIMEOUT
        retries = retries if retries is not None else settings.UDP_MAX_RETRIES

        last_error = None
        for attempt in range(retries):
            try:
                return await self._send_once(data, timeout)
            except asyncio.TimeoutError as e:
                last_error = e
                if attempt < retries - 1:
                    await asyncio.sleep(0.05)  # 重试前等待 50ms
                continue

        raise ConnectionError(f"UDP 通信超时（已重试 {retries} 次）") from last_error

    async def _send_once(self, data: bytes, timeout: float) -> Tuple[bytes, float]:
        """单次发送并等待响应"""
        # 从报文提取请求 ID
        req_id = self._extract_request_id(data)

        # 创建等待响应的 Future
        future = asyncio.get_event_loop().create_future()
        self._pending_requests[req_id] = future

        try:
            start_time = time.time()
            self._transport.sendto(data)
            response = await asyncio.wait_for(future, timeout=timeout)
            elapsed_ms = (time.time() - start_time) * 1000
            return response, elapsed_ms
        finally:
            self._pending_requests.pop(req_id, None)

    async def send_raw(self, data: bytes) -> None:
        """
        发送原始 UDP 数据（不等待响应）
        用于调试终端的单向发送

        Args:
            data: 要发送的字节数据
        """
        if not self._is_connected:
            raise ConnectionError("UDP 未连接")
        self._transport.sendto(data)

    def _extract_request_id(self, data: bytes) -> int:
        """从报文中提取请求 ID（字节 14-15）"""
        if len(data) >= 16:
            return int.from_bytes(data[14:16], byteorder="little")
        return 0

    def set_data_received_callback(self, callback: Optional[Callable]):
        """
        设置数据接收回调
        当收到非请求响应的数据时触发（如心跳响应、异步推送）

        Args:
            callback: 回调函数，接收 (data: bytes, addr: tuple) 参数
        """
        self._on_data_received = callback

    def get_stats(self) -> dict:
        """获取通信统计数据"""
        if self._protocol:
            return self._protocol.get_stats()
        return {
            "bytes_sent": 0,
            "bytes_received": 0,
            "packets_sent": 0,
            "packets_received": 0,
            "errors": 0,
        }

    def reset_stats(self):
        """重置通信统计数据"""
        if self._protocol:
            self._protocol.reset_stats()


class _YERCUDPProtocol(asyncio.DatagramProtocol):
    """UDP 协议处理器（内部类）"""

    def __init__(self, client: UDPClient):
        self._client = client
        self._transport: Optional[asyncio.DatagramTransport] = None
        # 统计数据
        self._bytes_sent = 0
        self._bytes_received = 0
        self._packets_sent = 0
        self._packets_received = 0
        self._errors = 0

    def connection_made(self, transport: asyncio.DatagramTransport):
        """连接建立"""
        self._transport = transport

    def datagram_received(self, data: bytes, addr: Tuple[str, int]):
        """接收到 UDP 数据"""
        self._bytes_received += len(data)
        self._packets_received += 1

        # 提取请求 ID，匹配等待中的请求
        req_id = self._client._extract_request_id(data)
        future = self._client._pending_requests.get(req_id)
        if future and not future.done():
            future.set_result(data)
            return

        # 非请求响应数据，触发回调
        if self._client._on_data_received:
            try:
                self._client._on_data_received(data, addr)
            except Exception:
                self._errors += 1

    def error_received(self, exc: Exception):
        """连接错误"""
        self._errors += 1

    def connection_lost(self, exc: Optional[Exception]):
        """连接断开"""
        self._client._is_connected = False

    def get_stats(self) -> dict:
        return {
            "bytes_sent": self._bytes_sent,
            "bytes_received": self._bytes_received,
            "packets_sent": self._packets_sent,
            "packets_received": self._packets_received,
            "errors": self._errors,
        }

    def reset_stats(self):
        self._bytes_sent = 0
        self._bytes_received = 0
        self._packets_sent = 0
        self._packets_received = 0
        self._errors = 0


# 全局 UDP 客户端单例
udp_client = UDPClient()
