"""
操作日志服务
查询/导出/自动记录
"""
from typing import Optional, List
from datetime import datetime
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.operation_log import OperationLog
from app.models.user import User


async def query_logs(
    db: AsyncSession,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    operation_type: Optional[str] = None,
    user_id: Optional[int] = None,
    page: int = 1,
    page_size: int = 20,
    current_user_id: Optional[int] = None,
    is_admin: bool = False,
) -> tuple:
    """
    查询操作日志（分页）
    普通用户只能查看自己的日志，管理员可查看全部

    Args:
        db: 数据库会话
        start_time: 开始时间
        end_time: 结束时间
        operation_type: 操作类型
        user_id: 用户 ID 筛选
        page: 页码
        page_size: 每页条数
        current_user_id: 当前用户 ID（非管理员时按此筛选）
        is_admin: 是否为管理员

    Returns:
        (日志列表, 总数)
    """
    conditions = []

    if start_time:
        conditions.append(OperationLog.timestamp >= start_time)
    if end_time:
        conditions.append(OperationLog.timestamp <= end_time)
    if operation_type:
        conditions.append(OperationLog.operation_type == operation_type)
    if user_id:
        conditions.append(OperationLog.user_id == user_id)
    if not is_admin and current_user_id:
        conditions.append(OperationLog.user_id == current_user_id)

    query = select(OperationLog)
    if conditions:
        query = query.where(and_(*conditions))

    # 总数
    count_query = select(func.count()).select_from(OperationLog)
    if conditions:
        count_query = count_query.where(and_(*conditions))
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    query = query.order_by(OperationLog.timestamp.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    logs = result.scalars().all()

    return list(logs), total


async def get_log_stats(
    db: AsyncSession,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> dict:
    """获取日志统计信息"""
    conditions = []
    if start_time:
        conditions.append(OperationLog.timestamp >= start_time)
    if end_time:
        conditions.append(OperationLog.timestamp <= end_time)

    # 总操作数
    query = select(func.count()).select_from(OperationLog)
    if conditions:
        query = query.where(and_(*conditions))
    total_result = await db.execute(query)
    total = total_result.scalar() or 0

    # 按操作类型统计
    # 简化实现：返回总数
    return {
        "total": total,
        "by_type": {},
        "by_user": {},
    }
