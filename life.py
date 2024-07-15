#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File         :life.py
@Description  :应用启动生命周期，包括启动前运行、停止后运行的内容
@Time         :2024/07/15 09:28:13
@Author       :Thornhill
@Version      :1.0
'''


from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.config import settings
from core.database.base import HZDB





async def startup() -> None:
    """启动前运行"""
    HZDB(settings.DB.model_dump())
    


        
async def shutdown() -> None:
    """停止时运行"""
    pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    """生命周期函数"""
    await startup()
    yield
    await shutdown()