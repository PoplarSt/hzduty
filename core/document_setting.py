#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :document_setting.py
@Description  :为fastapi注册自定义的rapidoc文档,并提供CustomHTTPBasic，基于软件管理的账号验证
@Time         :2024/07/15 09:00:41
@Author       :Thornhill
@Version      :1.0
"""



from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse, StreamingResponse
# from models.auth.dependence import hzsysLoginProxy
from base64 import b64decode
from typing import Optional

from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED


class CustomHTTPBasic(HTTPBasic):
    """为适配公司中文账号，自定义HTTPBasic验证，支持中文用户名密码，解码方式从ascii改为utf8"""

    async def __call__(  # type: ignore
        self, request: Request
    ) -> Optional[HTTPBasicCredentials]:
        authorization = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if self.realm:
            unauthorized_headers = {"WWW-Authenticate": f'Basic realm="{self.realm}"'}
        else:
            unauthorized_headers = {"WWW-Authenticate": "Basic"}
        if not authorization or scheme.lower() != "basic":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers=unauthorized_headers,
                )
            else:
                return None
        invalid_user_credentials_exc = HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers=unauthorized_headers,
        )
        try:
            data = b64decode(param).decode("utf-8")
        except (ValueError, UnicodeDecodeError):
            raise invalid_user_credentials_exc  # noqa: B904
        username, separator, password = data.partition(":")
        if not separator:
            raise invalid_user_credentials_exc
        return HTTPBasicCredentials(username=username, password=password)


document_basic_auth = CustomHTTPBasic()





AXIOS_API_TEMPLATE = """

export const %s = data => {
    /*%s*/
    return request({
        url: '%s',
        method: '%s',
        data,
    })
}
"""

templates = Jinja2Templates(directory="templates")


def register_custom_document(app: FastAPI, prefix="", title=""):
    """
    为fastapi注册自定义的rapidoc文档
    """
    
    
    @app.get("/index.js", summary="🟢【🛠️】api")
    async def api_generate() -> StreamingResponse:
        """
        生成前端用的API接口
        """

        def iterfile():
            yield """import request from '@/utils/request'"""
            for i in app.routes:
                if i.name in ["openapi", "openapi_json", "api_generate", "rapidoc"]:
                    continue
                t = AXIOS_API_TEMPLATE % (
                    i.name,
                    i.endpoint.__doc__,
                    prefix + i.path,
                    list(i.methods)[0],
                )
                yield t

        return StreamingResponse(iterfile(), media_type="text/javascript")

    # 文档页面地址
    @app.get("/rapidoc", response_class=HTMLResponse, include_in_schema=False)
    async def rapidoc(
        request: Request,
        # credentials: Annotated[HTTPBasicCredentials, Depends(document_basic_auth)],
    ) -> str:
        
        # TODO: 公司账号验证，暂时注释
        # try:
        #     response = await hzsysLoginProxy(credentials.username, credentials.password)
        # except Exception:
        #     response = None
        # # print(response)
        # if response is None:
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="用户名密码不正确",
        #         headers={"WWW-Authenticate": "Basic"},
        #     )
        
        openapi_url = f"{prefix}{app.openapi_url}"
        return templates.TemplateResponse(
            request=request,
            name="document_template.html",
            context={"openapi_url": openapi_url, "title": title},
        )

    # 文档页面地址
    @app.get("/openapi.json", include_in_schema=False)
    async def openapi_json(
        # credentials: Annotated[HTTPBasicCredentials, Depends(document_basic_auth)], 
    ):
        # for i in app.routes:
        #     print(i)
        return app.openapi_url

    return app
