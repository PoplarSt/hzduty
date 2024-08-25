from typing import Optional, Dict
from pydantic import BaseModel
from typing import List
class UserID(BaseModel):
    用户ID: int

class OrgI(UserID):
    组织ID: int
    组织名称: str
    行政区划ID: str
    # 用户ID: int
class UserI(UserID):
    角色ID: int
    角色名称: str
    角色描述: str
    角色标识: str
class Token(BaseModel):
    access_token: str
    token_type: str
class Org(BaseModel):
    组织ID: int
    组织名称: str
    行政区划ID: str
class User(BaseModel):
    角色ID: int
    角色名称: str
    角色描述: str
    角色标识: str
class UserBase(BaseModel):
    用户ID: int | None = None
    用户编号: str
    账号: str
    # 密码: str
    姓名: str
    用户类别ID: int
    联系电话: str
    邮箱地址: str
    角色: list[UserI]
    组织: list[OrgI]

class UserCreate(UserBase):
    密码: str
    # 有密码


# class User(UserBase):
#     class Config:
#         from_attributes = True
class Response(BaseModel):
    code: str
    data: Dict
    message: str
