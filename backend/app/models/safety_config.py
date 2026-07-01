"""
安全配置模型
使用 JSONB 存储各轴软件限位
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base


class SafetyConfig(Base):
    """安全配置表"""
    __tablename__ = "safety_config"

    id = Column(Integer, primary_key=True, autoincrement=True)
    max_speed_percent = Column(Integer, default=50, nullable=False)
    require_confirm = Column(Boolean, default=True, nullable=False)
    axis_limits = Column(JSONB, default=dict, nullable=True)
    # 默认各轴限位范围
    # {"j1": {"min": -180, "max": 180}, "j2": {...}, ...}
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False,
    )

    def __repr__(self):
        return f"<SafetyConfig(id={self.id}, max_speed={self.max_speed_percent}%)>"
