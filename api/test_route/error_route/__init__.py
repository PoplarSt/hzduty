from fastapi import APIRouter
from .params import router as params_router

router = APIRouter()

router.include_router(params_router, prefix="/params")