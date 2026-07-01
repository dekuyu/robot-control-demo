"""
报警相关 Schema
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class AlarmResponse(BaseModel):
    """报警信息响应"""
    id: int
    alarm_code: str
    alarm_level: str = "warning"
    description: Optional[str] = None
    is_active: bool = True
    occurred_at: Optional[datetime] = None
    cleared_at: Optional[datetime] = None


class AlarmResetRequest(BaseModel):
    """报警复位请求"""
    confirm: bool = Field(default=True, description="确认故障已排除")


class AlarmResetResponse(BaseModel):
    """报警复位响应"""
    reset: bool = True
    message: str = "报警已复位"


class AlarmNotificationConfig(BaseModel):
    """报警通知配置"""
    email: Optional[str] = None
    webhook_url: Optional[str] = None
    enabled: bool = False
