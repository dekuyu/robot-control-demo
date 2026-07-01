"""
安全相关 Schema
"""
from typing import Optional, Dict, List
from pydantic import BaseModel, Field


class AxisLimit(BaseModel):
    """轴限位配置"""
    min: float = -180.0
    max: float = 180.0


class SafetyCheckResult(BaseModel):
    """安全检查结果"""
    servo_ok: bool = False
    mode_ok: bool = False
    alarm_ok: bool = False
    speed_ok: bool = False
    operator_confirmed: bool = False
    all_passed: bool = False
    failures: List[str] = []


class SafetyConfigUpdate(BaseModel):
    """安全配置更新请求"""
    max_speed_percent: Optional[int] = Field(None, ge=0, le=100)
    require_confirm: Optional[bool] = None


class LimitUpdate(BaseModel):
    """轴限位更新请求"""
    axis_limits: Dict[str, AxisLimit] = Field(
        default_factory=lambda: {},
        description="示例: {'j1': {'min': -180, 'max': 180}, 'j2': {...}}"
    )


class SafetyConfigResponse(BaseModel):
    """安全配置响应"""
    id: int
    max_speed_percent: int = 50
    require_confirm: bool = True
    axis_limits: Dict[str, AxisLimit] = {}
    updated_by: Optional[int] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class EmergencyStopResponse(BaseModel):
    """急停响应"""
    stopped: bool = True
    message: str = "急停已激活"
