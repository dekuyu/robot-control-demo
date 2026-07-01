"""
通用响应模型
API 统一响应格式: {code, data, message}
"""
from typing import Optional, Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """API 通用响应"""
    code: int = 0
    message: Optional[str] = None
    data: Optional[T] = None

    @classmethod
    def success(cls, data: T = None, message: str = "操作成功") -> "ApiResponse[T]":
        """构建成功响应"""
        return cls(code=0, message=message, data=data)

    @classmethod
    def error(cls, code: int = 1, message: str = "操作失败") -> "ApiResponse":
        """构建错误响应"""
        return cls(code=code, message=message, data=None)


class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应"""
    code: int = 0
    message: Optional[str] = None
    data: Optional[List[T]] = None
    total: int = 0
    page: int = 1
    page_size: int = 20


class ErrorResponse(BaseModel):
    """错误响应"""
    code: int
    message: str
    error_code: Optional[str] = None
