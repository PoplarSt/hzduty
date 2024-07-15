import traceback
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from core.exception.pydantic_message_ext import convert_validation_errors

from fastapi.encoders import jsonable_encoder


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    """兜底的错误处理"""
    # logger.error(exc)
    print(exc)
    traceback.print_exc()
    return JSONResponse(
        {
            # "error": f"internal server error {exc}",
            "message": "服务器错误",
            "data": None,
            "code": "200002",
        },
        status_code=503,
    )


async def params_error_handler(_: Request, exc) -> JSONResponse:
    """参数错误"""
    errors = convert_validation_errors(exc)
    print(exec)
    return JSONResponse(
        jsonable_encoder(
            {
                "error": errors,
                "message": "参数错误",
                "data": None,
                "code": "100005",
            }
        ),
        status_code=200,
    )
    
async def authorization_error_handler(_: Request, exc) -> JSONResponse:
    """参数错误"""
    print(exc)
    traceback.print_exc()
    return JSONResponse(
        {
            "error": f"{exc}",
            "message": "用户登录信息失效，请重新登录",
            "data": None,
            "code": "100003",
        },
        status_code=200,
    )

async def not_found_error(_: Request, exc) -> JSONResponse:
    """参数错误"""
    print(exc.code)
    traceback.print_exc()
    return JSONResponse(
        {
            "error": f"{exc}",
            "message": f"{exc}不存在",
            "data": None,
            "code": exc.code,
        },
        status_code=200,
    )
