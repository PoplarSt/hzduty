#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File         :router_ext.py
@Description  :子应用注册工具，将各功能分隔为子应用，方便管理和部署，减少项目的耦合度。
@Time         :2024/07/15 09:03:08
@Author       :Thornhill
@Version      :1.0
'''



from fastapi import FastAPI
from core.exception import register_error_handler
from core.document_setting import register_custom_document
from core.utils.health_check import ensure_unique_route_names, simplify_operation_ids

def get_description() -> str:
    """
    获取项目的描述信息作为文档目录
    """
    description = ""
    with open("readme.md", "r", encoding='utf-8') as f:
        description = f.read()
    return description


def register_sub_app(
    app, api_router, prefix="/api", description="", ** kwargs
):
    # 取消默认的接口文档功能
    description = description or get_description()
    
    sub_app = FastAPI(docs_url=None, redoc_url=None, description=description,**kwargs)
    
    sub_app.include_router(api_router)
    
    sub_app = register_error_handler(sub_app)

    sub_app = register_custom_document(sub_app, prefix=prefix, title=kwargs["title"])
    
    simplify_operation_ids(sub_app)
    ensure_unique_route_names(sub_app)
    
    app.mount(prefix, sub_app)
    
    print(f"注册应用：{prefix}")

    return app
