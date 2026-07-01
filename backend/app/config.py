"""
应用配置模块
使用 Pydantic Settings 从 .env 文件和环境变量加载配置
生产环境必须通过环境变量覆盖敏感配置
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """应用全局配置"""

    # ===== 数据库配置 =====
    # 默认连接字符串仅用于本地开发，生产环境必须通过环境变量覆盖
    DATABASE_URL: str = "postgresql+asyncpg://robot_user:robot_123456@localhost:5432/robot_control"

    # ===== 安全配置 =====
    SECRET_KEY: str = "yrc1000-robot-control-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ===== 机器人默认连接配置 =====
    ROBOT_DEFAULT_IP: str = "192.168.255.1"
    ROBOT_DEFAULT_PORT: int = 10040
    ROBOT_LOCAL_PORT: int = 0

    # ===== 服务配置 =====
    SERVER_PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # ===== 性能配置 =====
    # UDP 通信超时（秒）
    UDP_TIMEOUT: float = 0.5
    # UDP 最大重试次数
    UDP_MAX_RETRIES: int = 3
    # 状态轮询间隔（秒）
    STATUS_POLL_INTERVAL: float = 0.02  # 20ms
    # 力矩轮询间隔（秒）
    TORQUE_POLL_INTERVAL: float = 0.05  # 50ms
    # 数据库连接池大小
    DB_POOL_SIZE: int = 20
    # 数据库连接溢出大小
    DB_MAX_OVERFLOW: int = 10

    # ===== 调试终端配置 =====
    TERMINAL_SEND_RATE_LIMIT: int = 10  # 次/秒
    PACKET_LOG_RETENTION_DAYS: int = 180

    # ===== 安全限制配置 =====
    # 全局最大速度百分比（默认50%）
    GLOBAL_SPEED_LIMIT: int = 50
    # 登录失败锁定次数
    MAX_LOGIN_ATTEMPTS: int = 5
    # 登录锁定时间（分钟）
    LOGIN_LOCK_MINUTES: int = 15

    @property
    def cors_origin_list(self) -> List[str]:
        """解析 CORS 来源列表"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# 全局配置实例
settings = Settings()
