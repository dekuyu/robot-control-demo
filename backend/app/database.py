"""
数据库连接模块
使用 SQLAlchemy 2.0 async 引擎 + asyncpg 驱动
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings


class Base(DeclarativeBase):
    """SQLAlchemy ORM 基类"""
    pass


# 创建异步数据库引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # 生产环境关闭 SQL 日志
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,  # 连接前检查可用性
)

# 创建异步会话工厂
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    """
    获取数据库会话的依赖注入函数
    用于 FastAPI Depends()
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def check_db_connection() -> bool:
    """
    数据库连接健康检查
    返回 True 表示连接正常
    """
    try:
        async with engine.connect() as conn:
            await conn.execute(
                __import__("sqlalchemy").text("SELECT 1")
            )
        return True
    except Exception:
        return False


async def init_db():
    """
    初始化数据库，创建所有表
    注意：生产环境应使用 Alembic 迁移
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """关闭数据库连接"""
    await engine.dispose()
