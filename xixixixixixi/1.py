import time
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from api.hzduty.settings.classes.interface import QueryClassesByOrgId
from api.hzduty.settings.classes.schemas import *
from core.database import HZDUTY
from models.hzduty.mdoel import D01值班班次类型
from api.hzduty.settings.classes.model import 班次,班次类型
router = APIRouter(tags=["班次管理"])


# @router.get(
#     "/query",
#     summary="根据班组ID查询班次",
# )
#
# async def query_classes_settings(ID:int, db=Depends(HZDUTY.session)):
#     query = select(班次表1).filter(班次表1.班组ID == ID)
#     r = await db.scalars(query)
#     return r.all()
@router.get(
    "/query/type",
    summary="班次类型查询"
)
async def get_shifts(clas_type: str=None , db=Depends(HZDUTY.session)):
    if clas_type:
        # 查询特定类型的班次
        query=select(班次).filter(班次.type_name == clas_type)
        shifts = await db.scalars(query)
    else:
        # 查询所有班次
        query=select(班次)
        shifts = await db.scalars(query)
    return shifts.all()

# @router.post(
#     "/...",
#     summary="查ID查班次类型"
# )
# async def query_id(zone_id:str,db=Depends(HZDUTY.session)):
#     query=select(班次类型.值班班次类型ID).filter(班次类型.行政区划==zone_id&&班次类型.值班班次类型='节假日班次')
#     query=await db.scalars(query)
#     data=query.all()
#     return data
# @router.post(
#     "/12232",
#     summary="all"
# )
# async def query_all(act:str, clas:str, db=Depends(HZDUTY.session)):
#     班次.type
#     班次.type_name




@router.post(
    "add_normal",
    status_code=201,
    summary="添加平常班次"
)
async def add_normal_settings(act:str, clas:str,db=Depends(HZDUTY.session)):
  try:
    act_time = datetime.strptime(act, '%H:%M:%S').time()
    # end_time = datetime.strptime(clas.end, '%H:%M').time()
    new_event = 班次(type_name='平时班次',班次名称=clas,开始时间=act,type=None)
    db.add(new_event)
    await db.commit()
    await db.refresh(new_event)
    return new_event
  except ValueError as e:
    raise HTTPException(status_code=400, detail="无效的时间格式")
@router.post(
    "add_holiday",
    status_code=201,
    summary="添加节假班次"
)
async def add_holiday_settings(act:str, clas:str, db=Depends(HZDUTY.session)):
  try:
    act_time = datetime.strptime(act, '%H:%M:%S').time()
    new_event = 班次(type_name='节假日班次',班次名称=clas,开始时间=act,type=None)
    db.add(new_event)
    await db.commit()
    await db.refresh(new_event)
    return new_event
  except ValueError as e:
    raise HTTPException(status_code=400, detail="无效的时间格式")

@router.delete(
      "/del_normal",
            summary="删除班次"
  )
async def delete_teams(id:int,db=Depends(HZDUTY.session)):
      item = await db.scalars(select(班次).filter(班次.值班班次ID == id))
      await db.delete(item.first())
      await db.commit()
      return  id

@router.post("/shift-types/",
            summary="读取",
            # response_model=Response
            )
async def read_shift_types(zone_id:str,db=Depends(HZDUTY.session)):
    # 读取所有班次类型及其班次
    query = select(班次类型).filter(班次类型.行政区划 == zone_id).options(joinedload(班次类型.班次))
    db_shift_types= await db.scalars(query)
    unique_shift_types = [st for st in db_shift_types.unique().all()]

    shift_types = [
        ShiftType(
            值班班次类型=st.值班班次类型,
            值班班次类型ID=st.值班班次类型ID,
            可删除=st.可删除,
            班次=[Shift(值班班次ID=s.值班班次ID, 开始时间=s.开始时间, 班次名称=s.班次名称) for s in st.班次]
        )
        for st in unique_shift_types
    ]
    # 创建响应模型
    response = Response(code="000000", data=shift_types, message="操作成功")
    return response
