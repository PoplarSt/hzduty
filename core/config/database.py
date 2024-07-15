from typing import Literal
from pydantic import BaseModel
from sqlalchemy import Enum


class DB_TYPE(str, Enum):
    """数据库类型"""
    MYSQL = "mysql"
    DAMENG = "dameng"


class RelationalDB(BaseModel):
    """数据库配置"""

    TYPE: Literal["mysql", "dameng"] = "mysql"
    HOST: str = "db"
    PORT: int = 3306
    USER: str = "root"
    PASSWORD: str = "root"
    CHARSET: str = "utf8mb4"
    AUTO_COMMIT: bool = True
    POOL_SIZE: int = 50
    CONNECT_TIMEOUT: int = 3
    DATABASE: str = "db"
    ECHO: bool = False


class DBSettings(BaseModel):
    """数据库配置"""

    hzduty: RelationalDB = RelationalDB()
    # hzadp: RelationalDB = RelationalDB()
    # hzshield: RelationalDB = RelationalDB()
    # hzalarm: RelationalDB = RelationalDB()
    # hzgrid: RelationalDB = RelationalDB()
    # HZSHIELD: HZSHIELD = HZSHIELD()
    # HZALARM: HZALARM = HZALARM()
