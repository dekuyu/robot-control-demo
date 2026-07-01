"""
位置与坐标相关 Schema
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class PositionPosture(BaseModel):
    """位置姿态"""
    joints: dict = Field(
        default_factory=lambda: {
            "j1": 0.0, "j2": 0.0, "j3": 0.0,
            "j4": 0.0, "j5": 0.0, "j6": 0.0,
        }
    )
    end_coords: dict = Field(
        default_factory=lambda: {
            "x": 0.0, "y": 0.0, "z": 0.0,
            "rx": 0.0, "ry": 0.0, "rz": 0.0,
        }
    )


class PositionCreate(BaseModel):
    """创建命名点位"""
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    p_variable_index: Optional[int] = Field(None, ge=0, le=127)
    posture: PositionPosture


class PositionUpdate(BaseModel):
    """更新命名点位"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    posture: Optional[PositionPosture] = None


class PositionResponse(BaseModel):
    """命名点位响应"""
    id: int
    name: str
    description: Optional[str] = None
    p_variable_index: Optional[int] = None
    posture: PositionPosture
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PositionExportRequest(BaseModel):
    """点位导出请求"""
    format: str = Field(default="json", pattern="^(json|csv)$")


class PositionImportResponse(BaseModel):
    """点位导入响应"""
    imported_count: int = 0
    errors: List[str] = []
