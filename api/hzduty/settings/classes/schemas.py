from datetime import time
from typing import List

from pydantic import BaseModel


class Shift(BaseModel):
    值班班次ID: int
    开始时间: time
    班次名称: str

    # @classmethod
    # def parse_time(cls, time_str: str) -> datetime:
    #     return datetime.strptime(time_str, '%H:%M:%S')
    #
    # @property
    # def 开始时间(self) -> datetime:
    #     return self.parse_time(self.开始时间)

# 定义 Pydantic 模型来表示班次类型
class ShiftType(BaseModel):
    值班班次类型: str
    值班班次类型ID: int
    可删除: int
    班次: List[Shift]

# 定义 Pydantic 模型来表示整个响应
class Response(BaseModel):
    code: str
    data: List[ShiftType]
    message: str


