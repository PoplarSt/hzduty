from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from api.hzduty.settings.teams.schemas import DutyGroup, DutyLeader, Member, ResponseData
from core.database import HZDUTY
from .model import  *

router = APIRouter(tags=["Test"])
@router.post(
             "/teamstest/",
             summary="读取",
)
async def query_teams_type(zone_id:int,db=Depends(HZDUTY.session)):
   query=select(班组).filter(班组.行政区划==zone_id).options(joinedload(班组.组长领导),joinedload(班组.排班成员班组成员))
   db_teams_type=await db.scalars(query)
   unique_teams_type=[tt for tt in db_teams_type.unique()]
   for tt in unique_teams_type:
       for t in tt.组长领导:
         if t.type==1:
             duty_leader1 = {
           "姓名": t.姓名,
           "用户ID": t.duty_leader_id
           }
         else:
             duty_leader2 = {
                 "姓名": t.姓名,
                 "用户ID": t.duty_leader_id
             }
   teams_type=[
       DutyGroup(
           值班单位=tt.值班单位,
           值班班组ID=tt.值班班组ID,
           # 值班组长=({"姓名": t.姓名,"用户ID": t.duty_leader_id} for t in tt.组长领导 if t.type==1),
           # 值班领导=({"姓名": t.姓名,"用户ID": t.duty_leader_id} for t in tt.组长领导 if t.type==0),
           值班组长= duty_leader2,
           值班领导= duty_leader1,
           排班成员=[Member(姓名=m.姓名,用户ID=m.member_id)for m in tt.排班成员班组成员],
           班组成员=[Member(姓名=m.姓名,用户ID=m.member_id)for m in tt.排班成员班组成员]
       )for tt in unique_teams_type
]
   response=ResponseData(code="000000",data=teams_type,message="操作成功")
   return response
