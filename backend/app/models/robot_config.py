"""
机器人连接配置模型
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.database import Base


class RobotConfig(Base):
    """机器人连接配置表"""
    __tablename__ = "robot_config"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), default="YRC1000", nullable=False)
    ip_address = Column(String(15), nullable=False, default="192.168.255.1")
    port = Column(Integer, default=10040, nullable=False)
    local_port = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False,
    )

    def __repr__(self):
        return f"<RobotConfig(id={self.id}, ip='{self.ip_address}:{self.port}')>"
