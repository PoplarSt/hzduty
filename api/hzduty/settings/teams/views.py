from fastapi import APIRouter, Depends
from api.hzduty.settings.teams.schemas import  Response
from core.database import HZDUTY
from .crud import query_teams
from .model import *
from ..classes.interface import OrgID

router = APIRouter(tags=["班组管理"])
@router.post("/teams_type/",
             summary="读取")
async def query_teams1(id:OrgID ,db=Depends(HZDUTY.session)):
    zone_id=id.组织ID
    teams_type = await query_teams(zone_id=zone_id, db=db)
    response = Response(code="000000", data=teams_type, message="操作成功")
    return response