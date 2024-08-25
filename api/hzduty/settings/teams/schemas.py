from typing import Dict

from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    name: str
    user_id: int

class DutyLeader(BaseModel):

    姓名: str
    用户ID: int

class Member(BaseModel):
    姓名: str
    用户ID: int

class DutyGroup(BaseModel):
    值班单位: str
    值班班组ID: int
    值班组长:Dict
    值班领导:Dict
    序号:int
    排班成员: list[Member]
    班组名称:str
    班组成员: list[Member]

class Response(BaseModel):
    code: str
    data: list[DutyGroup]
    message: str

# 使用示例


# 将字典数据转换为 Pydantic 模型



