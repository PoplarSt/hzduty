from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, delete, and_
from sqlalchemy.orm import joinedload

from api.hzduty.settings.teams.schemas import DutyGroup, DutyLeader, Member, ResponseData
from core.database import HZDUTY
from .model import  *
from .schemas import *

router = APIRouter(tags=["Test"])
@router.post(
             "/teamstest/",
             summary="读取",
)
async def query_teams_type(zone_id:int,new_data: list[ShiftType],db=Depends(HZDUTY.session)):
    query = select(班次类型).filter(班次类型.行政区划 == zone_id).options(joinedload(班次类型.班次))
    db_shift_types = await db.scalars(query)

    shift_type_id_exists = {}
    for st in new_data:
        if st.值班班次类型ID:
            shift_id_exists = []
            new_shift = []

            for shift in st.班次:
                if shift.值班班次ID:
                    shift_id_exists.append(shift.值班班次ID)
                else:
                    new_shift.append(shift)

            shift_type_id_exists[st.值班班次类型ID] = {
                "shift_id_exists": shift_id_exists,
                "new_shift": new_shift
            }

        else:
            new_shift_type = 班次类型(
                ** st.model_dump()
            )
            db.add(new_shift_type)


    # unique_shift_types = [st for st in db_shift_types.unique()]
    for shift_type in db_shift_types.unique():
        if shift_type.值班班次类型ID not in shift_type_id_exists.keys():
            db.delete(shift_type)
        else:
            s = shift_type_id_exists[shift_type.值班班次类型ID]
            for shift in shift_type.班次:
                if shift.值班班次ID not in s["shift_id_exists"]:
                    db.delete(shift)

            for j in s["new_shift"]:
                shift_type.班次.append(班次(**j.model_dump()))

    await db.commit()

    return
async def query_teams_type(zone_id:int,new_data:list[ShiftType],db=Depends(HZDUTY.session)):
    query = select(班次类型).filter(班次类型.行政区划 == zone_id).options(joinedload(班次类型.班次))
    db_shift_types = await db.scalars(query)

    shift_type_id_exists = {}
    for st in new_data:
        if st.值班班次类型ID:
            shift_id_exists = []
            new_shift = []

            for shift in st.班次:
                if shift.值班班次ID:
                    shift_id_exists.append(shift.值班班次ID)
                else:
                    new_shift.append(shift)

            shift_type_id_exists[st.值班班次类型ID] = {
                "shift_id_exists": shift_id_exists,
                "new_shift": new_shift
            }
            print(shift_type_id_exists)

        else:
            new_shift_type = 班次类型(
                ** st.model_dump()
            )
            db.add(new_shift_type)


    # unique_shift_types = [st for st in db_shift_types.unique()]
    for shift_type in db_shift_types.unique():
        if shift_type.值班班次类型ID not in shift_type_id_exists.keys():
            db.delete(shift_type)
        else:
            s = shift_type_id_exists[shift_type.值班班次类型ID]
            for shift in shift_type.班次:
                if shift.值班班次ID not in s["shift_id_exists"]:
                    db.delete(shift)

            for j in s["new_shift"]:
                shift_type.班次.append(班次(**j.model_dump()))
                # print(j)
                # print(**j.model_dump())

    await db.commit()

    return