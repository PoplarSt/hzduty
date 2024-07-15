#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File         :schema.py
@Description  :返回值的封装结构
@Time         :2024/07/15 09:06:09
@Author       :Thornhill
@Version      :1.0
'''


from datetime import datetime
from typing import Any, Generic, TypeVar
from pydantic import BaseModel, ConfigDict, Field
from core.config import settings

M = TypeVar("M", bound=BaseModel)


class HZResponseMeta(BaseModel):
    model_config = ConfigDict(from_attributes = True, json_encoders={datetime: lambda x: x.strftime(settings.DATETIME_FORMAT)})

    code: str = Field(default="000000", example="000000")
    msg: str = Field(default="请求成功", example="请求成功")
    data: Any | None = None


class HZResponseModel(HZResponseMeta, Generic[M]):
    data: M 


class PaginationMeta(BaseModel):
    current_page: int = Field(alias="当前页码", example="1")
    total_num: int = Field(alias="总条目数", example="1000")
    total_page: int = Field(alias="总页数", example="100")
    page_size: int = Field(alias="每页数量", example="10")


class Pagination(BaseModel, Generic[M]):
    data: list[M] = Field(alias="数据")
    pagination: PaginationMeta | None = Field(alias="分页信息", default=None)