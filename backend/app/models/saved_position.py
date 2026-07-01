"""
命名点位模型
使用 JSONB 存储姿态数据
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, func
from app.database import Base


class SavedPosition(Base):
    """保存的命名点位表"""
    __tablename__ = "saved_positions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    p_variable_no = Column(Integer, nullable=True)
    # 末端坐标
    x_mm = Column(Float, nullable=True)
    y_mm = Column(Float, nullable=True)
    z_mm = Column(Float, nullable=True)
    rx_deg = Column(Float, nullable=True)
    ry_deg = Column(Float, nullable=True)
    rz_deg = Column(Float, nullable=True)
    # 关节角度
    j1_deg = Column(Float, nullable=True)
    j2_deg = Column(Float, nullable=True)
    j3_deg = Column(Float, nullable=True)
    j4_deg = Column(Float, nullable=True)
    j5_deg = Column(Float, nullable=True)
    j6_deg = Column(Float, nullable=True)
    j7_deg = Column(Float, nullable=True)
    posture = Column(String(50), nullable=True)
    tool_no = Column(Integer, nullable=True)
    coordinate_no = Column(Integer, nullable=True)
    created_by = Column(Integer, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False,
    )

    def __repr__(self):
        return f"<SavedPosition(id={self.id}, name='{self.name}')>"
