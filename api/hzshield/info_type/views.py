from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from core.database import HZSHIELD
from core.exception.errors import NotFoundError
from models.hzshield.model import N01信息类型, N11信息拟制


router = APIRouter(tags=["信息类型"])


@router.post(
    "/query",
    summary="查询信息类型",
)
async def query_info_type(db=Depends(HZSHIELD.session)):
    """
    测查询信息类型
    """
    query = select(N01信息类型)
    r = await db.scalars(query)
    return r.all()



class IDQuery(BaseModel):
    id: str = Field(example="【32010520240703001】", description="信息类型ID")


@router.post(
    "/info/template",
    summary="查询信息的信息模板",
)
async def query_info_template(
    schema: IDQuery, db=Depends(HZSHIELD.session)
) :
    """
    查询信息的信息模板
    """
    query = (
        select(N11信息拟制)
        .where(N11信息拟制.信息ID == schema.id)
        .options(joinedload(N11信息拟制.n01信息模板))
    )
    r = await db.scalar(query)
    
    # 查询不到则抛出NotFound错误
    if not r:
        raise NotFoundError("信息模板")
    
    return r
