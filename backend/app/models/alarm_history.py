"""
报警历史模型
"""
import enum
from datetime import datetime, timezone
from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime, Enum, func
from app.database import Base


class AlarmLevel(str, enum.Enum):
    """报警级别枚举"""
    CRITICAL = "critical"   # 重度
    WARNING = "warning"     # 轻度
    INFO = "info"           # 信息


class AlarmHistory(Base):
    """报警历史表"""
    __tablename__ = "alarm_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    alarm_code = Column(String(10), nullable=False)
    alarm_level = Column(Enum(AlarmLevel), default=AlarmLevel.WARNING, nullable=False)
    description = Column(Text, nullable=True)
    occurred_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    cleared_at = Column(DateTime(timezone=True), nullable=True)
    cleared_by = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<AlarmHistory(id={self.id}, code='{self.alarm_code}', level='{self.alarm_level}')>"
