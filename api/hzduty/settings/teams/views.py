from fastapi import APIRouter, Depends
from sqlalchemy import select
from core.database import HZDUTY
from models.hzduty.mdoel import D01值班班次类型


router = APIRouter(tags=["班组管理"])


@router.post(
    "/add",
    summary="创建值班班组",
)
async def add_duty_team(db=Depends(HZDUTY.session)):
    """
    创建值班班组
    根据组织ID创建一个值班班组
    @param db: 数据库会话
    @return: 创建的班组信息
    """
    query = select(D01值班班次类型)
    r = await db.scalars(query)
    return r.all()
