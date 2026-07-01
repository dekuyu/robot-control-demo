"""
UDP/串口调试终端 API 路由
报文发送/配置/日志查询/命令模板
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user, get_current_engineer_or_admin
from app.schemas.common import ApiResponse, PaginatedResponse
from app.schemas.terminal import (
    TerminalSendRequest, TerminalSendResponse,
    TerminalConfigResponse, TerminalStatsResponse,
    PacketLogResponse, TerminalTemplateResponse,
)
from app.services import terminal_service
from app.utils.logging_utils import log_operation
from app.core.exceptions import AppException

router = APIRouter()


@router.post("/send", response_model=ApiResponse[TerminalSendResponse])
async def send_hex(
    request: TerminalSendRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_engineer_or_admin),
):
    """
    发送十六进制报文（需要工程师或管理员权限）
    默认发送频率限制 ≤10 次/秒
    """
    try:
        result = await terminal_service.send_hex_data(
            request.hex_data,
            request.wait_response,
            current_user.id,
            current_user.username,
        )

        # 记录操作日志
        await log_operation(
            db, current_user.id, current_user.username,
            "TERMINAL_SEND", target="udp_debug",
            parameters={"hex": request.hex_data[:100]},
            robot_response=result.get("response_hex"),
        )

        # 保存报文日志
        from app.services.udp_client import udp_client
        await terminal_service.save_packet_log(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            direction="send",
            target_ip=udp_client.robot_ip,
            target_port=udp_client.robot_port,
            raw_hex=request.hex_data.upper(),
            data_length=result["data_length"],
            response_time_ms=result.get("response_time_ms"),
        )

        if result.get("response_hex"):
            await terminal_service.save_packet_log(
                db=db,
                user_id=current_user.id,
                username=current_user.username,
                direction="receive",
                target_ip=udp_client.robot_ip,
                target_port=udp_client.robot_port,
                raw_hex=result["response_hex"],
                data_length=len(result["response_hex"]) // 3,
            )

        return ApiResponse.success(data=TerminalSendResponse(**result))
    except ValueError as e:
        return ApiResponse.error(message=str(e))
    except AppException as e:
        return ApiResponse.error(message=e.message)


@router.get("/stats", response_model=ApiResponse[TerminalStatsResponse])
async def get_stats():
    """获取终端统计信息"""
    stats = terminal_service.get_terminal_stats()
    return ApiResponse.success(data=TerminalStatsResponse(**stats))


@router.post("/stats/reset", response_model=ApiResponse)
async def reset_stats(current_user=Depends(get_current_user)):
    """重置终端统计"""
    terminal_service.reset_terminal_stats()
    return ApiResponse.success(message="统计已重置")


@router.get("/config", response_model=ApiResponse[TerminalConfigResponse])
async def get_terminal_config():
    """获取终端连接配置"""
    from app.services.udp_client import udp_client
    return ApiResponse.success(data=TerminalConfigResponse(
        target_ip=udp_client.robot_ip,
        target_port=udp_client.robot_port,
        connected=udp_client.is_connected,
    ))


@router.get("/templates", response_model=ApiResponse)
async def get_templates():
    """获取 YERC 命令模板列表"""
    templates = terminal_service.get_templates()
    return ApiResponse.success(data=templates)


@router.get("/packet-logs", response_model=PaginatedResponse[PacketLogResponse])
async def query_packet_logs(
    start_time: str = Query(None),
    end_time: str = Query(None),
    direction: str = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """查询报文日志（分页）"""
    from app.utils.time_utils import from_iso
    st = from_iso(start_time) if start_time else None
    et = from_iso(end_time) if end_time else None

    logs, total = await terminal_service.query_packet_logs(
        db, st, et, direction, page=page, page_size=page_size,
    )
    items = [PacketLogResponse.model_validate(log) for log in logs]
    return PaginatedResponse(data=items, total=total, page=page, page_size=page_size)
