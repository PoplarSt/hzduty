import os
import subprocess
from typing import Literal
from fastapi import APIRouter
from pydantic import Field, RootModel

from core.database.base import HZDB
from core.response import HZResponse
from core.response.schema import HZResponseModel


router = APIRouter(tags=["数据库配置"])

class Databases(RootModel):
    root: list[str] = Field(..., description="list of database")


@router.get(
    "/database",
    summary="查询全部数据库",
)
async def query_databases() -> HZResponseModel[Databases]:
    """
    查询全部数据库
    """
    return await HZResponse.success(data = list(HZDB.DATABASES.keys()))


# @router.get(
#     "/tables",
#     summary="查询全部数据表",
# )
# async def query_tables(database:str) -> list[str]:
#     """
#     查询全部数据表
#     """
#     return HZDB.DATABASES.keys()

@router.post(
    "/create",
    summary="生成数据库模型",
)
async def create_models(
    database: str,
    table: list[str] | None,
    file_name: str = "generate",
    generator: Literal[
        "sqlmodels", "dataclasses", "declarative", "tables"
    ] = "declarative",
):
    """
    查询全部数据表
    """
    
    uri = HZDB.DATABASES[database].sync_uri
    
    if table:
        table_str = "--tables " + ",".join(table)
    else:
        table_str = ""
        
    file_path = f"./models/auto_code/{file_name}"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
        
    
        
    cmd = f"sqlacodegen {uri} --generator {generator} {table_str} --outfile {file_path}/model.py" 
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    print(result.stdout)
    
    return 

