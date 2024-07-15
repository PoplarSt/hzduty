#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File         :health_check.py
@Description  :系统健康检查，在app启动前调用，也可仅在开发时使用
@Time         :2024/07/15 09:03:47
@Author       :Thornhill
@Version      :1.0
'''



from fastapi import FastAPI
from fastapi.routing import APIRoute

# from backend.common.exception import errors


def ensure_unique_route_names(app: FastAPI) -> None:
    """
    检查路由名称是否唯一

    :param app:
    :return:
    """
    temp_routes = set()
    for route in app.routes:
        if isinstance(route, APIRoute):
            if route.name in temp_routes:
                print(f'Duplicate route name: {route.name}')
                raise ValueError(f'Non-unique route name: {route.name}')
            temp_routes.add(route.name)


def simplify_operation_ids(app: FastAPI) -> None:
    """
    简化操作 ID，以便生成的客户端具有更简单的 api 函数名称

    :param app:
    :return:
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name

# async def http_limit_callback(request: Request, response: Response, expire: int):
#     """
#     请求限制时的默认回调函数

#     :param request:
#     :param response:
#     :param expire: 剩余毫秒
#     :return:
#     """
#     expires = ceil(expire / 1000)
#     raise errors.HTTPError(code=429, msg='请求过于频繁，请稍后重试', headers={'Retry-After': str(expires)})
