"""
中间件模块
CORS、请求日志、速率限制
"""
import time
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import settings


def setup_cors(app):
    """配置 CORS 中间件"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """请求日志中间件：记录每个 HTTP 请求的耗时"""
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000  # 转换为毫秒

        # 添加响应头：X-Process-Time
        response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
        return response
