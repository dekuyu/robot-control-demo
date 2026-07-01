"""
WebSocket 推送消息 Schema
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


# === WebSocket 消息类型 ===
class WSMessageType:
    """WebSocket 消息类型常量"""
    ROBOT_STATUS = "robot_status"
    ROBOT_POSITION = "robot_position"
    ROBOT_TORQUE = "robot_torque"
    ALARM_UPDATE = "alarm_update"
    CONNECTION_UPDATE = "connection_update"
    SAFETY_ALERT = "safety_alert"
    ERROR = "error"
    PACKET_LOG = "packet_log"


class WSMessage(BaseModel):
    """WebSocket 通用推送消息结构"""
    type: str
    timestamp: str  # ISO 8601 UTC
    data: Dict[str, Any] = Field(default_factory=dict)


# === 各类型具体数据 ===

class WSRobotStatusData(BaseModel):
    """机器人核心状态"""
    servo_on: bool = False
    running_mode: str = "unknown"
    alarm_active: bool = False
    speed_percent: int = 0
    executing_program: Optional[str] = None


class WSRobotPositionData(BaseModel):
    """机器人位置数据"""
    joints: Dict[str, float] = Field(default_factory=dict)
    end_coords: Dict[str, float] = Field(default_factory=dict)


class WSRobotTorqueData(BaseModel):
    """各轴力矩数据"""
    torques: List[float] = Field(default_factory=list)


class WSAlarmData(BaseModel):
    """报警数据"""
    alarms: List[Dict[str, Any]] = Field(default_factory=list)
    has_active_alarm: bool = False


class WSConnectionData(BaseModel):
    """连接状态数据"""
    connected: bool = False
    last_heartbeat: Optional[str] = None


class WSSafetyAlertData(BaseModel):
    """安全告警数据"""
    alert_type: str
    message: str
    severity: str = "warning"  # critical / warning / info
