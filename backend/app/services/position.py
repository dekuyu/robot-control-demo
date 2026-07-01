"""
位置与坐标管理服务
命名点位 CRUD、P 变量读写、导入导出
"""
from typing import Optional, List
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.saved_position import SavedPosition
from app.models.user import User
from app.services.udp_client import udp_client
from app.services.yerc_protocol import yerc_protocol
from app.core.exceptions import PositionError, RobotNotConnectedError


async def get_positions(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 20,
    search: Optional[str] = None,
) -> tuple[List[SavedPosition], int]:
    """获取命名点位列表（分页）"""
    query = select(SavedPosition)
    if search:
        query = query.where(SavedPosition.name.ilike(f"%{search}%"))

    # 计算总数
    count_query = select(SavedPosition).with_only_columns(
        __import__("sqlalchemy").func.count()
    )
    if search:
        count_query = count_query.where(SavedPosition.name.ilike(f"%{search}%"))

    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    query = query.order_by(SavedPosition.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    positions = result.scalars().all()

    return list(positions), total


async def create_position(db: AsyncSession, data: dict, user_id: int) -> SavedPosition:
    """创建命名点位"""
    posture = data.get("posture", {})
    joints = posture.get("joints", {})
    end_coords = posture.get("end_coords", {})

    position = SavedPosition(
        name=data["name"],
        description=data.get("description"),
        p_variable_no=data.get("p_variable_index"),
        x_mm=end_coords.get("x"),
        y_mm=end_coords.get("y"),
        z_mm=end_coords.get("z"),
        rx_deg=end_coords.get("rx"),
        ry_deg=end_coords.get("ry"),
        rz_deg=end_coords.get("rz"),
        j1_deg=joints.get("j1"),
        j2_deg=joints.get("j2"),
        j3_deg=joints.get("j3"),
        j4_deg=joints.get("j4"),
        j5_deg=joints.get("j5"),
        j6_deg=joints.get("j6"),
        j7_deg=joints.get("j7"),
        created_by=user_id,
    )
    db.add(position)
    await db.flush()
    return position


async def update_position(
    db: AsyncSession, position_id: int, data: dict
) -> Optional[SavedPosition]:
    """更新命名点位"""
    result = await db.execute(
        select(SavedPosition).where(SavedPosition.id == position_id)
    )
    position = result.scalar_one_or_none()
    if not position:
        return None

    for key, value in data.items():
        if hasattr(position, key) and value is not None:
            setattr(position, key, value)

    await db.flush()
    return position


async def delete_position(db: AsyncSession, position_id: int) -> bool:
    """删除命名点位"""
    result = await db.execute(
        select(SavedPosition).where(SavedPosition.id == position_id)
    )
    position = result.scalar_one_or_none()
    if position:
        await db.delete(position)
        await db.flush()
        return True
    return False


async def get_current_position() -> dict:
    """获取机器人当前姿态"""
    if not udp_client.is_connected:
        # 返回空姿态
        return _empty_posture()

    try:
        # 读取位置数据
        cmd = yerc_protocol.build_read_position()
        response, _ = await udp_client.send_and_receive(cmd)
        parsed = yerc_protocol.parse_response(response)

        if parsed["is_success"]:
            angles = yerc_protocol.parse_joint_angles(parsed["data"])
            return _build_posture(angles)
    except Exception:
        pass

    return _empty_posture()


async def read_p_variable(index: int) -> dict:
    """读取 P 变量位置数据"""
    if not udp_client.is_connected:
        raise RobotNotConnectedError()

    try:
        cmd = yerc_protocol.build_read_p_variable(index)
        response, _ = await udp_client.send_and_receive(cmd)
        parsed = yerc_protocol.parse_response(response)

        if parsed["is_success"]:
            angles = yerc_protocol.parse_joint_angles(parsed["data"])
            return _build_posture(angles)
    except Exception as e:
        raise PositionError(f"读取 P 变量失败: {str(e)}")

    return _empty_posture()


async def write_p_variable(index: int, posture_data: dict) -> dict:
    """写入 P 变量"""
    if not udp_client.is_connected:
        raise RobotNotConnectedError()

    try:
        joints = posture_data.get("joints", {})
        joint_list = [
            joints.get("j1", 0), joints.get("j2", 0),
            joints.get("j3", 0), joints.get("j4", 0),
            joints.get("j5", 0), joints.get("j6", 0),
            joints.get("j7", 0),
        ]
        cmd = yerc_protocol.build_write_p_variable_joint(index, joint_list)
        response, _ = await udp_client.send_and_receive(cmd)
        parsed = yerc_protocol.parse_response(response)
        if parsed["is_success"]:
            return posture_data
    except Exception as e:
        raise PositionError(f"写入 P 变量失败: {str(e)}")

    raise PositionError("写入 P 变量失败：机器人返回错误")


def _build_posture(angles: List[float]) -> dict:
    """从角度列表构建姿态字典"""
    return {
        "joints": {
            "j1": angles[0] if len(angles) > 0 else 0,
            "j2": angles[1] if len(angles) > 1 else 0,
            "j3": angles[2] if len(angles) > 2 else 0,
            "j4": angles[3] if len(angles) > 3 else 0,
            "j5": angles[4] if len(angles) > 4 else 0,
            "j6": angles[5] if len(angles) > 5 else 0,
            "j7": angles[6] if len(angles) > 6 else 0,
        },
        "end_coords": {"x": 0, "y": 0, "z": 0, "rx": 0, "ry": 0, "rz": 0},
    }


def _empty_posture() -> dict:
    return _build_posture([0, 0, 0, 0, 0, 0, 0])
