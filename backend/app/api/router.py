"""
API 主路由聚合
将所有子路由 include 到主路由
"""
from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.robot import router as robot_router
from app.api.safety import router as safety_router
from app.api.control import router as control_router
from app.api.position import router as position_router
from app.api.variable import router as variable_router
from app.api.alarm import router as alarm_router
from app.api.log import router as log_router
from app.api.user import router as user_router
from app.api.ws import router as ws_router
from app.api.terminal import router as terminal_router

api_router = APIRouter()

# 注册所有子路由
api_router.include_router(auth_router, prefix="/api/auth", tags=["认证"])
api_router.include_router(robot_router, prefix="/api/robot", tags=["机器人连接"])
api_router.include_router(safety_router, prefix="/api/safety", tags=["安全管理"])
api_router.include_router(control_router, prefix="/api/control", tags=["机械臂控制"])
api_router.include_router(position_router, prefix="/api/positions", tags=["坐标与位置"])
api_router.include_router(variable_router, prefix="/api/variables", tags=["变量读写"])
api_router.include_router(alarm_router, prefix="/api/alarms", tags=["报警管理"])
api_router.include_router(log_router, prefix="/api/logs", tags=["操作日志"])
api_router.include_router(user_router, prefix="/api/users", tags=["用户管理"])
api_router.include_router(ws_router, prefix="/ws", tags=["WebSocket"])
api_router.include_router(terminal_router, prefix="/api/terminal", tags=["调试终端"])
