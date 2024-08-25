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

from api.hzduty.settings.auth.crud import init_admin_user
from core.config import settings
from core.database import HZDUTY
from core.database.base import HZDB
# 假设 HZDUTY.session() 返回一个异步生成器
async def get_db_session():
    async for db_session in HZDUTY.session():
        return db_session  # 只获取第一个会话并退出循环
    # 可以添加逻辑来处理没有会话的情况
    raise ValueError("No database session available")




async def startup() -> None:
    """启动前运行"""
    HZDB(settings.DB.model_dump())


    db_session = await get_db_session()  # 获取数据库会话
    try:
        await init_admin_user(db=db_session)  # 初始化管理员用户
    finally:
            # 这里不关闭会话，因为它将被应用的其他部分使用
        pass


async def shutdown() -> None:
    """停止时运行"""
    pass


@asynccontextmanager
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # 使用 next() 和 async for 获取异步生成器的第一个值
        db_session = await next(HZDUTY.session())
        yield db_session
        await startup(db_session)  # 假设 startup 需要 db_session
    finally:
        await db_session.close()  # 确保关闭数据库会话
        await shutdown()