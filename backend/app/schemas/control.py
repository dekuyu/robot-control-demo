"""
控制指令相关 Schema
"""
from typing import Optional, List
from pydantic import BaseModel, Field


class ServoCommand(BaseModel):
    """伺服控制命令"""
    action: str = Field(..., pattern="^(on|off)$")


class ProgramCommand(BaseModel):
    """程序控制命令"""
    action: str = Field(..., pattern="^(start|stop|pause|resume|reset)$")
    program_name: Optional[str] = None


class JogRequest(BaseModel):
    """点动控制请求"""
    axis: int = Field(..., ge=1, le=7, description="轴编号: 1~7")
    direction: str = Field(..., pattern="^(positive|negative)$", description="方向")
    speed_percent: int = Field(default=10, ge=1, le=100, description="速度百分比")


class JogStopRequest(BaseModel):
    """停止点动请求"""
    axis: int = Field(..., ge=1, le=7)


class IncrementRequest(BaseModel):
    """增量移动请求"""
    axis: int = Field(..., ge=1, le=7, description="轴编号")
    increment_deg: float = Field(..., description="增量角度（度）")


class TargetMoveRequest(BaseModel):
    """目标角度运动请求"""
    target: dict = Field(..., description="目标位置: {'j1': 45.0, ...} 或 {'x': 100.0, ...}")
    speed_percent: int = Field(default=30, ge=1, le=100)
    coordinate_type: str = Field(default="joint", pattern="^(joint|cartesian)$")


class CartesianRequest(BaseModel):
    """直角坐标控制请求"""
    axis: str = Field(..., pattern="^(x|y|z|rx|ry|rz)$")
    value: float = Field(...)
    speed_percent: int = Field(default=30, ge=1, le=100)


class SpeedRequest(BaseModel):
    """速度设置请求"""
    speed_percent: int = Field(..., ge=0, le=100, description="速度百分比: 0~100")
