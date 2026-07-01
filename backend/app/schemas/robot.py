"""
机器人相关 Schema
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class RobotConfigCreate(BaseModel):
    """机器人连接配置创建"""
    name: str = Field(default="YRC1000", max_length=50)
    ip: str = Field(default="192.168.255.1", pattern=r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    port: int = Field(default=10040, ge=1, le=65535)
    local_port: int = Field(default=0, ge=0, le=65535)


class RobotConfigResponse(BaseModel):
    """机器人连接配置响应"""
    id: int
    name: str
    ip: str
    port: int
    local_port: int
    is_active: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RobotConnectRequest(BaseModel):
    """连接机器人请求"""
    ip: str = Field(default="192.168.255.1")
    port: int = Field(default=10040, ge=1, le=65535)


class JointAngles(BaseModel):
    """关节角度"""
    j1: float = 0.0
    j2: float = 0.0
    j3: float = 0.0
    j4: float = 0.0
    j5: float = 0.0
    j6: float = 0.0
    j7: Optional[float] = None


class EndCoords(BaseModel):
    """末端笛卡尔坐标"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    rx: float = 0.0
    ry: float = 0.0
    rz: float = 0.0


class RobotStatusResponse(BaseModel):
    """机器人完整状态响应"""
    connected: bool = False
    servo_on: bool = False
    running_mode: str = "unknown"
    alarm_active: bool = False
    speed_percent: int = 0
    joints: Optional[JointAngles] = None
    end_coords: Optional[EndCoords] = None
    torques: Optional[List[float]] = None
    executing_program: Optional[str] = None
    last_heartbeat: Optional[datetime] = None


class HeartbeatResponse(BaseModel):
    """心跳状态响应"""
    alive: bool = False
    last_beat: Optional[datetime] = None
