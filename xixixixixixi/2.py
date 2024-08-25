import databases
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, Delete
from sqlalchemy.orm import Session

from api.hzduty.settings.teams import crud, model
from api.hzduty.settings.teams.schemas import Teams
from core.database import HZDUTY
from api.hzduty.settings.teams.model import 班组表
from api.hzduty.settings.teams.model import 组织表

router = APIRouter(tags=["班组管理"])


@router.get(
    "/team/query",
    summary="查询",
)
async def query_team(db=Depends(HZDUTY.session)):
    query = select(班组表)
    r = await db.scalars(query)
    return r.all()


@router.get(
    "/team/query_one",
    summary="查询一条",
)
async def query_one(ID:int,db=Depends(HZDUTY.session)):
    team = await db.scalars(select(班组表).filter(班组表.班组ID == ID))
    return team.first()
    # team=db.query(班组表).filter(班组表.班组ID==ID).first()
    # return await team


@router.delete(
    "/team/delete",
    summary="删除记录"
)
async def delete_team(ID:int,db=Depends(HZDUTY.session)):
    item = await db.scalars(select(班组表).filter(班组表.班组ID == ID))
    await db.delete(item.first())
    await db.commit()
    return ID
    # if not item1:
    #     raise HTTPException(status_code=404, detail="Team not found")
    # delete_statement = Delete(班组表).where(班组表.班组ID == ID)
    # await db.execute(delete_statement)
    # await db.commit()
    # return {"message": "Team deleted successfully", "team_id": ID}



@router.post(
    "/team/add",
    summary="添加数据"
)
async def add_one(team:Teams,db=Depends(HZDUTY.session)):
    team =班组表(班组ID=team.ID,班组名称=team.name,值班领导=team.leader,值班单位=team.organization,班组成员=team.people,值班组长=team.teamer)
    db.add(team)
    await db.commit()
    db.refresh(team)
    return team
@router.put(
    "/team/update",
    summary="更新一条记录"
)
async def update_one(ID:int,teamer:str,leader:str,people:str,organization:str,db=Depends(HZDUTY.session)):
    team = await db.scalars(select(班组表).filter(班组表.班组ID == ID))
    team=team.first()
    team.值班组长=teamer
    team.值班领导=leader
    team.班组成员=people
    team.值班单位=organization
    await db.commit()
    db.refresh(team)
    return team
@router.get(
    "/org/query",
    summary="岗位查询人员"
)
async def query_org(job_type:str,db=Depends(HZDUTY.session)):
        query=select(组织表.组织成员).filter(组织表.岗位职责==job_type)
        orgs = await db.scalars(query)
        return orgs.all()

