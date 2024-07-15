from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    name: str = Field(alias="姓名")
    password: str = Field(alias="密码", min_length=8)  