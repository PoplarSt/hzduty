from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, delete, and_
from sqlalchemy.orm import joinedload

from core.database import HZDUTY
from .model import  *
from .schemas import Response, ShiftType

router = APIRouter(tags=["Test"])
@router.post(
             "/teamstest/",
             summary="读取",
    response_model=Response,
)

async def query_teams_type123(zone_id:int,db=Depends(HZDUTY.session))->Response:
    # 定义查询，包括急切加载班次
    query = select(班次类型).filter(班次类型.行政区划 == zone_id).options(joinedload(班次类型.班次))
    db_shift_types = await db.scalars(query)
    results = [st for st in db_shift_types.unique()]
    shift_type_list = [ShiftType(**result) for result in results]
    # 创建 Response 对象
    response = Response(
        code="000000",
        data=shift_type_list,  # 转换为列表
        message="操作成功"
    )
    return response