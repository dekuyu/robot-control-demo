"""
操作日志相关 Schema
"""
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class LogQueryParams(BaseModel):
    """日志查询参数"""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    operation_type: Optional[str] = None
    user_id: Optional[int] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class LogResponse(BaseModel):
    """日志条目响应"""
    id: int
    timestamp: Optional[datetime] = None
    user_id: Optional[int] = None
    username: Optional[str] = None
    operation_type: str
    target: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    result: Optional[str] = "success"
    robot_response: Optional[str] = None

    class Config:
        from_attributes = True


class LogExportRequest(BaseModel):
    """日志导出请求"""
    format: str = Field(default="csv", pattern="^(csv|excel)$")
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    operation_type: Optional[str] = None


class LogStatsResponse(BaseModel):
    """日志统计响应"""
    total: int = 0
    by_type: Dict[str, int] = {}
    by_user: Dict[str, int] = {}
