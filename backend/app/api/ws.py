"""
WebSocket 端点
连接验证、心跳保持、数据推送
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import ws_get_current_user
from app.services.ws_manager import ws_manager

router = APIRouter()


@router.websocket("")
async def websocket_endpoint(
    websocket: WebSocket,
    db: AsyncSession = Depends(get_db),
):
    """
    WebSocket 连接端点
    连接地址: ws://host/ws?token={accessToken}
    认证失败时自动断开并返回错误码
    """
    user = await ws_get_current_user(websocket, db)
    if user is None:
        return

    await ws_manager.connect(websocket, user.id)

    try:
        # 保持连接，接收客户端消息（心跳等）
        while True:
            data = await websocket.receive_text()
            # 可以处理客户端消息，如心跳回复
            if data == "ping":
                await websocket.send_json({"type": "pong", "timestamp": ""})
    except WebSocketDisconnect:
        pass
    finally:
        ws_manager.disconnect(websocket)
