"""
报警服务模块
报警查询/历史/复位/通知配置
"""
from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.alarm_history import AlarmHistory, AlarmLevel
from app.services.udp_client import udp_client
from app.services.yerc_protocol import yerc_protocol
from app.services.robot import update_robot_status
from app.core.exceptions import RobotNotConnectedError


async def get_active_alarms(db: AsyncSession) -> List[dict]:
    """获取当前活跃报警（从机器人 + 数据库）"""
    alarms = []

    # 从机器人读取报警信息
    if udp_client.is_connected:
        try:
            cmd = yerc_protocol.build_read_alarm()
            response, _ = await udp_client.send_and_receive(cmd)
            parsed = yerc_protocol.parse_response(response)
            # 解析报警数据（具体格式需对照协议）
            if parsed["is_success"] and parsed["data"]:
                # 占位：解析报警信息
                pass
        except Exception:
            pass

    # 从数据库查询未清除的报警
    result = await db.execute(
        select(AlarmHistory)
        .where(AlarmHistory.cleared_at == None)
        .order_by(AlarmHistory.occurred_at.desc())
    )
    db_alarms = result.scalars().all()

    for alarm in db_alarms:
        alarms.append({
            "id": alarm.id,
            "alarm_code": alarm.alarm_code,
            "alarm_level": alarm.alarm_level.value,
            "description": alarm.description,
            "is_active": True,
            "occurred_at": alarm.occurred_at,
            "cleared_at": alarm.cleared_at,
        })

    return alarms


async def get_alarm_history(
    db: AsyncSession,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    level: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple:
    """查询报警历史（分页）"""
    conditions = []
    if start_time:
        conditions.append(AlarmHistory.occurred_at >= start_time)
    if end_time:
        conditions.append(AlarmHistory.occurred_at <= end_time)
    if level:
        conditions.append(AlarmHistory.alarm_level == AlarmLevel(level))

    query = select(AlarmHistory)
    if conditions:
        query = query.where(and_(*conditions))

    # 总数
    count_query = select(func.count()).select_from(AlarmHistory)
    if conditions:
        count_query = count_query.where(and_(*conditions))
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    query = query.order_by(AlarmHistory.occurred_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    alarms = result.scalars().all()

    alarm_list = []
    for alarm in alarms:
        alarm_list.append({
            "id": alarm.id,
            "alarm_code": alarm.alarm_code,
            "alarm_level": alarm.alarm_level.value,
            "description": alarm.description,
            "is_active": alarm.cleared_at is None,
            "occurred_at": alarm.occurred_at,
            "cleared_at": alarm.cleared_at,
        })

    return alarm_list, total


async def reset_alarms(db: AsyncSession, user_id: int) -> dict:
    """报警复位"""
    now = datetime.now(timezone.utc)

    # 清除数据库中所有未处理报警
    result = await db.execute(
        select(AlarmHistory).where(AlarmHistory.cleared_at == None)
    )
    active_alarms = result.scalars().all()
    for alarm in active_alarms:
        alarm.cleared_at = now
        alarm.cleared_by = user_id
    await db.flush()

    update_robot_status(alarm_active=False)
    return {"reset": True, "cleared_count": len(active_alarms)}
