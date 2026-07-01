"""
用户相关 Pydantic Schema
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """登录请求"""
    username: str = Field(..., min_length=2, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, max_length=128, description="密码")


class LoginResponse(BaseModel):
    """登录响应"""
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    user: "UserResponse"


class RefreshTokenRequest(BaseModel):
    """刷新 Token 请求"""
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    """刷新 Token 响应"""
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class UserCreate(BaseModel):
    """创建用户请求"""
    username: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)
    role: str = Field(default="operator", pattern="^(admin|operator|engineer|observer)$")


class UserUpdate(BaseModel):
    """更新用户请求"""
    username: Optional[str] = Field(None, min_length=2, max_length=50)
    role: Optional[str] = Field(None, pattern="^(admin|operator|engineer|observer)$")
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    """用户信息响应"""
    id: int
    username: str
    role: str
    is_active: bool
    is_locked: bool
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
