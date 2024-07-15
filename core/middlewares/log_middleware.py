#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File         :log_middleware.py
@Description  :操作日志中间件，为每个请求记录日志
@Time         :2024/07/15 09:07:01
@Author       :Thornhill
@Version      :1.0
'''


from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import Response, UploadFile
# from extension import hzdb
# from models.base import Z01AuditLog
from starlette.background import BackgroundTask


class OperateLogMiddleware(BaseHTTPMiddleware):
    
    """操作日志记录中间件"""
    WHITE_LIST = ["rapidoc", "swagger", "openapi.json"]

    # TODO: 测试它对于文件、socket等特殊接口的兼容性
    async def dispatch(self, request: Request, call_next) -> Response:
        
        # 不记录日志的白名单
        path = request.url.path
        for path_filter in self.WHITE_LIST:
            if path_filter in path:
                return await call_next(request)
            

        request.state.user = {}
        start_time = datetime.now()
        args = await self.get_request_args(request)

        # 执行路由
        response = await call_next(request)
        
        stop_time = datetime.now()
        process_time = (stop_time - start_time).total_seconds()
        response.headers["X-Process-Time"] = str(process_time)
        
        # user信息依赖于个depends存储的用户上下文信息
        user = request.state.user
        
        # 存储到hzsys数据库
        # if hzdb.has_db("hzsys_saas"):
        #     try:
        #         # 兼容路由名称中的特殊字符
        #         route_name = str(request.scope["route"].summary)
        #         route_name = route_name.split("】")[1] if "】" in route_name else route_name
                
        #         log_data = dict(
        #             URL=request.url.path,
        #             服务器IP=request.headers["host"],
        #             客户端IP=request.client.host,
        #             请求开始时间=start_time,
        #             请求结束时间=stop_time,
        #             请求耗时=str(int(process_time * 1000)),
        #             返回结果=str(),
        #             结果状态码=str(response.status_code),
        #             请求参数=args,
        #             接口名称=route_name
        #         )
                
        #         if user:
        #             log_data.update(
        #                 用户ID=user.get("id"),
        #                 用户=user.get("username"),
        #             )
                    
        #         back = BackgroundTask(self.save_log, log_data=log_data)
        #         await back()
        #         response.headers["X-Process-Log"] = "success"
                
        #     except Exception as e:
        #         print("log error:", e)
        #         response.headers["X-Process-Log"] = "failed"
                
        return response


    async def save_log(self, log_data:dict) -> None:
        """保存日志"""
        # async with hzdb("hzsys_saas").SessionLocal() as db_session:
        #     new = Z01AuditLog(**log_data)
        #     db_session.add(new)
        #     await db_session.commit()
        pass

    async def get_request_args(self, request: Request) -> dict:
        """获取请求参数"""
        args = dict(request.query_params)
        args.update(request.path_params)
        # Tip: .body() 必须在 .form() 之前获取
        # https://github.com/encode/starlette/discussions/1933
        body_data = await request.body()
        form_data = await request.form()
        if len(form_data) > 0:
            args.update(
                {
                    k: v.filename if isinstance(v, UploadFile) else v
                    for k, v in form_data.items()
                }
            )
        else:
            if body_data:
                json_data = await request.json()
                if not isinstance(json_data, dict):
                    json_data = {
                        f"{type(json_data)}_to_dict_data": (
                            json_data.decode("utf-8")
                            if isinstance(json_data, bytes)
                            else json_data
                        )
                    }
                args.update(json_data)
        return args