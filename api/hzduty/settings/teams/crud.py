from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from api.hzduty.settings.teams.schemas import DutyGroup,Member
from core.database import HZDUTY
from .model import *
async def query_teams(zone_id:int,db=Depends(HZDUTY.session)):
   query=select(班组).filter(班组.行政区划==zone_id).options(joinedload(班组.组长领导),joinedload(班组.排班成员班组成员))
   db_teams_type=await db.scalars(query)
   unique_teams_type=[tt for tt in db_teams_type.unique()]
   # unique_teams_type = db_teams_type.all()
   teams_type = []

   # 遍历每个班组，创建DutyGroup对象
   for team in  unique_teams_type:
       # 初始化值班组长和值班领导信息
       duty_leader1 = {}
       duty_leader2 = {}
       # 根据type区分值班组长和值班领导
       for leader in team.组长领导:
           if leader.type == 1:
               duty_leader1 = {
                   "姓名": leader.姓名,
                   "用户ID": leader.duty_leader_id
               }
           else:
               duty_leader2 = {
                   "姓名": leader.姓名,
                   "用户ID": leader.duty_leader_id
               }
               # 创建DutyGroup对象并添加到结果列表
       teams_type.append(DutyGroup(
           值班单位=team.值班单位,
           值班班组ID=team.值班班组ID,
           值班组长=duty_leader1,
           值班领导=duty_leader2,
           序号=team.序号,
           排班成员=[Member(姓名=m.姓名, 用户ID=m.member_id) for m in team.排班成员班组成员],
           班组名称=team.班组名称,
           # 假设 组成员与排班成员相同，如果不同，需要另外处理
           班组成员=[Member(姓名=m.姓名, 用户ID=m.member_id) for m in team.排班成员班组成员]
       ))

   # 创建响应数据

   return teams_type

