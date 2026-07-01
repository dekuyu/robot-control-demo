"""
操作日志模型
BigSerial 主键 + JSONB 参数存储
"""
from datetime import datetime, timezone
from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime, Index, func
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base


class OperationLog(Base):
    """操作日志表 - 记录所有控制操作"""
    __tablename__ = "operation_log"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    timestamp = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False,
        index=True,
    )
    user_id = Column(Integer, nullable=True, index=True)
    username = Column(String(50), nullable=True)
    operation_type = Column(String(30), nullable=False)
    target = Column(String(100), nullable=True)
    parameters = Column(JSONB, default=dict, nullable=True)
    result = Column(String(10), default="success", nullable=True)
    robot_response = Column(Text, nullable=True)

    # 复合索引
    __table_args__ = (
        Index("idx_oplog_timestamp", "timestamp"),
        Index("idx_oplog_user", "user_id"),
        Index("idx_oplog_type", "operation_type"),
    )

    def __repr__(self):
        return f"<OperationLog(id={self.id}, type='{self.operation_type}', user='{self.username}')>"
