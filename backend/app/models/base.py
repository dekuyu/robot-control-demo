"""
ORM 模型基类
提供通用的 id、created_at、updated_at 字段
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, func
from app.database import Base


class TimestampMixin:
    """时间戳混入类：自动管理创建时间和更新时间"""
    id = Column(Integer, primary_key=True, autoincrement=True)
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
