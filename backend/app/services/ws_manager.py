"""
WebSocket 连接管理器
管理所有客户端连接、广播、按用户推送
"""
import json
from typing import Dict, Set, Optional, Any
from fastapi import WebSocket
from app.schemas.ws import WSMessage
from app.utils.time_utils import utc_now_iso


class ConnectionManager:
    """
    WebSocket 连接管理器
    维护活跃连接列表，支持广播和定向推送
    """

    def __init__(self):
        # 存储活跃连接: {user_id: set(WebSocket)}
        self._connections: Dict[int, Set[WebSocket]] = {}
        # 存储连接对应的用户: {WebSocket: user_id}
        self._ws_to_user: Dict[WebSocket, int] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        """接受 WebSocket 连接"""
        await websocket.accept()

        if user_id not in self._connections:
            self._connections[user_id] = set()
        self._connections[user_id].add(websocket)
        self._ws_to_user[websocket] = user_id

    def disconnect(self, websocket: WebSocket):
        """断开 WebSocket 连接"""
        user_id = self._ws_to_user.pop(websocket, None)
        if user_id and user_id in self._connections:
            self._connections[user_id].discard(websocket)
            if not self._connections[user_id]:
                del self._connections[user_id]

    async def send_to_user(self, user_id: int, message: WSMessage):
        """向指定用户推送消息"""
        if user_id in self._connections:
            data = message.model_dump()
            dead_sockets = set()
            for ws in self._connections[user_id]:
                try:
                    await ws.send_json(data)
                except Exception:
                    dead_sockets.add(ws)
            # 清理断开的连接
            for ws in dead_sockets:
                self.disconnect(ws)

    async def broadcast(self, message: WSMessage):
        """向所有连接用户广播消息"""
        data = message.model_dump()
        dead_sockets = set()
        for user_id in list(self._connections.keys()):
            for ws in self._connections[user_id]:
                try:
                    await ws.send_json(data)
                except Exception:
                    dead_sockets.add(ws)

        for ws in dead_sockets:
            self.disconnect(ws)

    async def send_json(self, websocket: WebSocket, data: dict):
        """向指定 WebSocket 发送 JSON 数据"""
        try:
            await websocket.send_json(data)
        except Exception:
            self.disconnect(websocket)

    def get_connection_count(self) -> int:
        """获取当前活跃连接数"""
        return len(self._ws_to_user)

    def is_user_connected(self, user_id: int) -> bool:
        """检查用户是否有活跃连接"""
        return user_id in self._connections and len(self._connections[user_id]) > 0


# 全局 WebSocket 管理器单例
ws_manager = ConnectionManager()
