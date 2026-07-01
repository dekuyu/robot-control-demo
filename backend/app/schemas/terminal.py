"""
调试终端相关 Schema
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class TerminalSendRequest(BaseModel):
    """终端发送报文请求"""
    hex_data: str = Field(..., min_length=1, description="十六进制报文（可带空格）")
    wait_response: bool = Field(default=True, description="是否等待响应")


class TerminalSendResponse(BaseModel):
    """终端发送报文响应"""
    sent_hex: str
    response_hex: Optional[str] = None
    response_time_ms: Optional[float] = None
    data_length: int = 0
    success: bool = True


class TerminalConfigRequest(BaseModel):
    """终端连接配置请求"""
    target_ip: str = Field(default="192.168.255.1")
    target_port: int = Field(default=10040, ge=1, le=65535)
    local_port: int = Field(default=0, ge=0, le=65535)
    mode: str = Field(default="UDP", pattern="^(UDP|TCP|Serial)$")


class TerminalConfigResponse(BaseModel):
    """终端连接配置响应"""
    target_ip: str = "192.168.255.1"
    target_port: int = 10040
    local_port: int = 0
    mode: str = "UDP"
    connected: bool = False


class TerminalStatsResponse(BaseModel):
    """终端统计信息"""
    bytes_sent: int = 0
    bytes_received: int = 0
    packets_sent: int = 0
    packets_received: int = 0
    errors: int = 0


class PacketLogQueryParams(BaseModel):
    """报文日志查询参数"""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    direction: Optional[str] = Field(None, pattern="^(send|receive)$")
    target_ip: Optional[str] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class PacketLogResponse(BaseModel):
    """报文日志条目响应"""
    id: int
    timestamp: Optional[datetime] = None
    user_id: Optional[int] = None
    username: Optional[str] = None
    direction: str
    target_ip: Optional[str] = None
    target_port: Optional[int] = None
    raw_hex: str
    data_length: Optional[int] = None
    response_time_ms: Optional[int] = None

    class Config:
        from_attributes = True


class TerminalTemplateResponse(BaseModel):
    """命令模板响应"""
    name: str
    description: str
    command: str  # 十六进制命令
