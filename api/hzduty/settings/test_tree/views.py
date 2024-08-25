from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload, selectinload, Session

from api.hzduty.settings.classes.model import 班次
# from api.hzduty.settings.teams.model import 班组表
from api.hzduty.settings.test_tree.model import Node
# from core.database import HZDUTY
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# from api.hzduty.settings.classes.model import 班次表2,班次表1

engine = create_engine(f"mysql://root:123456@127.0.0.1/test")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_tables():
    Base.metadata.create_all(bind=engine)

async def get_params(
        page: Optional[int] = 1,
        size: Optional[int] = 10
):
    return {"size": size, "page": page}

router = APIRouter(tags=["树状结构"])


@router.get(
    "/tree",
    summary="生成树",
)
async def wozhenfule(db:Session = Depends(get_db)):
    # team = await db.scalars(select(班组表).filter(班组表.班组ID == ID))
    # return team.first()
    query=select(Node).options(joinedload(Node.children)).filter_by(p_id=None)
    root = db.scalars(query)
    tree_structure =  build_tree(root.first())
    print(tree_structure)
    return tree_structure


# def build_tree(node, level=0):
#     tree = f"{' ' * (level * 2)}{node.name}\n"
#     for child in node.children:
#          tree += build_tree(child, level + 1)
#     return  tree
# 字符串
def build_tree(node, level=0):
    tree = {'name': node.name, 'level': level}
    if node.children:
        tree['children'] = [build_tree(child, level + 1) for child in node.children]
    return tree
# 列表
@router.get(
    "/list",
    summary="分页"
)

async def list(params: dict= Depends(get_params), db: Session = Depends(get_db)):
    qcnt = db.query(func.count(班次.值班班次ID))
    q = db.query(班次)
    cnt = qcnt.scalar()
    data = q.limit(params["size"]).offset((params["page"] - 1) * params["page"]).all()

    return {"count": cnt, "list": data}
