"""
FastAPI 应用入口
路由注册 + 中间件 + 生命周期管理
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import settings
from app.core.middleware import setup_cors, RequestLoggingMiddleware
from app.core.exceptions import AppException
from app.core.error_codes import ERROR_CODES
from app.api.router import api_router
from app.database import check_db_connection, close_db, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    启动时：初始化数据库、检查连接
    关闭时：清理资源
    """
    # 启动时
    print("=" * 60)
    print("  YRC1000 Robot Control System - Starting...")
    print(f"  Server: http://0.0.0.0:{settings.SERVER_PORT}")
    print(f"  API Docs: http://localhost:{settings.SERVER_PORT}/docs")
    print("=" * 60)

    # 检查数据库连接
    db_ok = await check_db_connection()
    if db_ok:
        print("[OK] Database connection healthy")
    else:
        print("[WARN] Database connection failed - check DATABASE_URL")

    yield  # 服务运行中

    # 关闭时
    print("[INFO] Shutting down...")
    await close_db()
    print("[OK] Server stopped")


# 创建 FastAPI 应用
app = FastAPI(
    title="YRC1000 Robot Control System",
    description="安川 YRC1000 机械臂 UDP 远程控制系统",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# 配置 CORS
setup_cors(app)

# 添加请求日志中间件
app.add_middleware(RequestLoggingMiddleware)

# 注册主路由
app.include_router(api_router)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """统一的应用异常处理：转换为标准 API 响应"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": int(exc.error_code[1:]),
            "message": exc.message,
            "data": None,
        },
    )


@app.get("/", include_in_schema=False)
async def root():
    """健康检查端点"""
    db_ok = await check_db_connection()
    return {
        "name": "YRC1000 Robot Control System",
        "version": "1.0.0",
        "status": "running",
        "database": "connected" if db_ok else "error",
    }


@app.get("/health", include_in_schema=False)
async def health_check():
    """详细健康检查"""
    db_ok = await check_db_connection()
    return {
        "status": "healthy" if db_ok else "degraded",
        "database": {"status": "ok" if db_ok else "error"},
        "timestamp": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ).isoformat(),
    }
