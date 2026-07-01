"""
报文日志模型
记录 UDP 调试终端的每次收发
"""
from datetime import datetime, timezone
from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime, Index, func
from app.database import Base


class PacketLog(Base):
    """报文日志表 - 记录调试终端的所有收发"""
    __tablename__ = "packet_log"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    timestamp = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False,
    )
    user_id = Column(Integer, nullable=True)
    username = Column(String(50), nullable=True)
    direction = Column(String(10), nullable=False)  # 'send' 或 'receive'
    target_ip = Column(String(15), nullable=True)
    target_port = Column(Integer, nullable=True)
    raw_hex = Column(Text, nullable=False)  # 原始十六进制字符串
    data_length = Column(Integer, nullable=True)  # 数据长度（字节）
    response_time_ms = Column(Integer, nullable=True)  # 响应耗时

    __table_args__ = (
        Index("idx_packet_timestamp", "timestamp"),
        Index("idx_packet_user", "user_id"),
        Index("idx_packet_direction", "direction"),
    )

    def __repr__(self):
        return f"<PacketLog(id={self.id}, dir='{self.direction}', len={self.data_length})>"
