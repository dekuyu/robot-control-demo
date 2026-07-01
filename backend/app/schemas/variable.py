"""
变量读写相关 Schema
"""
from typing import Optional, List
from pydantic import BaseModel, Field


class VariableReadRequest(BaseModel):
    """读取变量请求"""
    var_type: str = Field(..., pattern="^(B|P|I|D|IO)$")
    index: int = Field(..., ge=0)


class VariableWriteRequest(BaseModel):
    """写入变量请求"""
    var_type: str = Field(..., pattern="^(B|P|IO|D)$")
    index: int = Field(..., ge=0)
    value: float = Field(...)


class VariableResponse(BaseModel):
    """变量响应"""
    var_type: str
    index: int
    value: float
    raw_hex: Optional[str] = None


class BatchReadRequest(BaseModel):
    """批量读取请求"""
    var_type: str = Field(default="B", pattern="^(B|P|I|D|IO)$")
    indices: List[int] = Field(..., description="变量编号列表")


class BatchReadResponse(BaseModel):
    """批量读取响应"""
    values: List[VariableResponse] = []
    total: int = 0


class IOResponse(BaseModel):
    """IO 信号响应"""
    index: int
    value: int = 0
    label: Optional[str] = None
