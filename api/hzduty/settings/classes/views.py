from fastapi import APIRouter, Depends
from sqlalchemy import select
from api.hzduty.settings.classes.interface import QueryClassesByOrgId
from core.database import HZDUTY
from models.hzduty.mdoel import D01值班班次类型


router = APIRouter(tags=["班次管理"])


@router.post(
    "/query",
    summary="根据组织ID查询班次",
)
async def query_classes_settings(schema: QueryClassesByOrgId, db=Depends(HZDUTY.session)):
    """
    测查询信息类型
    """
    query = select(D01值班班次类型).where(D01值班班次类型.组织ID == schema.组织ID)
    r = await db.scalars(query)
    return r.all()
