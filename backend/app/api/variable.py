"""
变量读写 API 路由
B/P/IO/I/D 变量读写
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.common import ApiResponse
from app.schemas.variable import (
    VariableWriteRequest, VariableResponse, BatchReadRequest, BatchReadResponse,
)
from app.services import variable as variable_service
from app.utils.logging_utils import log_operation
from app.core.exceptions import AppException

router = APIRouter()


@router.get("/b/{index}", response_model=ApiResponse[VariableResponse])
async def read_b_var(index: int):
    """读取 B 变量"""
    try:
        result = await variable_service.read_b_variable(index)
        return ApiResponse.success(data=VariableResponse(**result))
    except AppException as e:
        return ApiResponse.error(message=e.message)


@router.put("/b/{index}", response_model=ApiResponse[VariableResponse])
async def write_b_var(
    index: int, request: VariableWriteRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """写入 B 变量"""
    try:
        result = await variable_service.write_b_variable(index, int(request.value))
        await log_operation(
            db, current_user.id, current_user.username, "VAR_WRITE",
            target=f"B{index:03d}", parameters={"value": int(request.value)},
        )
        return ApiResponse.success(data=VariableResponse(**result))
    except AppException as e:
        return ApiResponse.error(message=e.message)


@router.post("/b/batch", response_model=ApiResponse[BatchReadResponse])
async def batch_read_b_vars(request: BatchReadRequest):
    """批量读取 B 变量"""
    try:
        results = await variable_service.batch_read_b_variables(request.indices)
        items = [VariableResponse(**r) for r in results]
        return ApiResponse.success(data=BatchReadResponse(values=items, total=len(items)))
    except AppException as e:
        return ApiResponse.error(message=e.message)


@router.get("/io/{index}", response_model=ApiResponse)
async def read_io(index: int):
    """读取 IO 信号"""
    try:
        result = await variable_service.read_io(index)
        return ApiResponse.success(data=result)
    except AppException as e:
        return ApiResponse.error(message=e.message)


@router.put("/io/{index}", response_model=ApiResponse)
async def write_io(
    index: int, request: dict,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """写入 IO 信号"""
    try:
        result = await variable_service.write_io(index, int(request.get("value", 0)))
        await log_operation(
            db, current_user.id, current_user.username, "IO_WRITE",
            target=f"IO_{index}", parameters=request,
        )
        return ApiResponse.success(data=result)
    except AppException as e:
        return ApiResponse.error(message=e.message)


@router.get("/i/{index}", response_model=ApiResponse)
async def read_i_var(index: int):
    """读取 I 变量"""
    try:
        result = await variable_service.read_i_variable(index)
        return ApiResponse.success(data=result)
    except AppException as e:
        return ApiResponse.error(message=e.message)


@router.get("/d/{index}", response_model=ApiResponse)
async def read_d_var(index: int):
    """读取 D 变量"""
    try:
        result = await variable_service.read_d_variable(index)
        return ApiResponse.success(data=result)
    except AppException as e:
        return ApiResponse.error(message=e.message)


@router.put("/d/{index}", response_model=ApiResponse)
async def write_d_var(
    index: int, request: VariableWriteRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """写入 D 变量"""
    try:
        result = await variable_service.write_d_variable(index, request.value)
        return ApiResponse.success(data=result)
    except AppException as e:
        return ApiResponse.error(message=e.message)
