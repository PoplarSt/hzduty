from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.config import settings
from core.middlewares.log_middleware import OperateLogMiddleware
from life import lifespan
from routers import register_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware



def register_middleware(app: FastAPI) -> FastAPI:
    # 支持跨域
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # 除了更新系统，都启用压缩中间件
    if settings.APP_NAME != "hzupdate":
        app.add_middleware(GZipMiddleware, minimum_size=1000)
    # 日志记录中间件
    app.add_middleware(OperateLogMiddleware)
    # app.add_middleware(PyInstrumentProfilerMiddleware)
    return app  


def create_app() -> FastAPI:
    """主程序注册"""
    app = FastAPI(lifespan=lifespan)

    register_router(app)
    
    register_middleware(app)
        
    # 挂载静态文件
    app.mount("/static", StaticFiles(directory="static"), name="static")


    return app


app = create_app()
