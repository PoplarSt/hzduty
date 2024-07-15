#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :routers.py
@Description  :各子软件的路由注册模块
@Time         :2024/07/15 09:30:07
@Author       :Thornhill
@Version      :1.0
"""

from fastapi import FastAPI

from core.router_ext import register_sub_app


def register_router(app: FastAPI) -> FastAPI:
    register_test_api(app)
    ...
    return app



def register_test_api(app: FastAPI) -> FastAPI:

    
    from api.test_route import router as test_api_router
    from api.auto_code import router as auto_code_router
    from api.hzshield import router as shield_router
    from api.hzduty import router as hzduty_router

    test_tags_metadata = [
        {
            "name": "测试应用",
            "description": """测试项目接口文档。""",
        }
    ]
    auto_tags_metadata = [
        {
            "name": "代码生成应用",
            "description": """测试项目接口文档。""",
        }
    ]
    hzshield_tags_metadata = [
        {
            "name": "护民之盾应用",
            "description": """测试项目接口文档。""",
        }
    ]
    
    app = register_sub_app(
        app,
        test_api_router,
        prefix="/api/v1.0/test",
        title="测试应用",
        version="1.0",
        openapi_tags=test_tags_metadata,
    )
    app = register_sub_app(
        app,
        auto_code_router,
        prefix="/api/v1.0/autoCode",
        title="测试代码生成",
        version="1.0",
        openapi_tags=auto_tags_metadata,
    )
    app = register_sub_app(
        app,
        shield_router,
        prefix="/api/v2.0/shield",
        title="测试护民之盾",
        version="2.0",
        openapi_tags=hzshield_tags_metadata,
    )
    app = register_sub_app(
        app,
        hzduty_router,
        prefix="/api/v2.0/duty",
        title="测试值班系统",
        version="2.0",
        openapi_tags=hzshield_tags_metadata,
    )
    return app