from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from api.hzduty.settings.classes.schemas import *
from core.database import HZDUTY
from api.hzduty.settings.classes.model import 班次类型


async def read_shift_types(zone_id: str, db=Depends(HZDUTY.session)):
    # 读取所有班次类型及其班次
    query = select(班次类型).filter(班次类型.行政区划 == zone_id).options(joinedload(班次类型.班次))
    db_shift_types = await db.scalars(query)
    unique_shift_types = [st for st in db_shift_types.unique()]

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

    return shift_types
