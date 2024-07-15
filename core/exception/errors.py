#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File         :errors.py
@Description  :自定义错误类，继承自Exception，在__init__.py中注册handler,在程序中主动raise抛出异常
@Time         :2024/07/15 09:07:52
@Author       :Thornhill
@Version      :1.0
'''


from typing import Any
from fastapi import BackgroundTasks

appmsg = {
    "000100": "账号不能为空",
    "000101": "请激活账号后登录",
    "000102": "账号被锁定，请解锁",
    "100001": "无效用户",
    "100002": "密码错误",
    "100003": "数字签名不合法",
    "100004": "没有数据访问权限",
    "100005": "无效的参数",
    "100006": "接口异常",
    "200001": "操作失败，详情：/n",
    "000000": "操作成功",
    "000001": "请求成功",
    "200002": "请求失败",
    "000103": "账号已存在",
}

class BaseException(Exception):
    code: str

    def __init__(
        self,
        msg: str = None,
        *,
        data: Any = None,
        background: BackgroundTasks | None = None,
    ):
        self.msg = msg
        self.data = data
        # The original background task: https://www.starlette.io/background/
        self.background = background


class ServerError(BaseException):
    code = "100003"

    def __init__(self, *, msg: str = '服务器错误', data: Any = None, background: BackgroundTasks | None = None):
        super().__init__(msg=msg, data=data, background=background)
        
        
class ForbiddenError(BaseException):
    code = "100003"

    def __init__(self, *, msg: str = 'Forbidden', data: Any = None, background: BackgroundTasks | None = None):
        super().__init__(msg=msg, data=data, background=background)


class NotFoundError(BaseException):
    """无数据错误， 如：查询不到数据，将对象名称填写在msg中"""
    code = "100003"

    def __init__(
        self,
        msg: str = "数据",
        *,
        data: Any = None,
        background: BackgroundTasks | None = None,
    ):
        super().__init__(msg=msg, data=data, background=background)


class AuthorizationError(BaseException):
    code = "100002"

    def __init__(
        self,
        msg: str = "",
        *,
        data: Any = None,
        background: BackgroundTasks | None = None,
    ):
        super().__init__(msg=msg, data=data, background=background)