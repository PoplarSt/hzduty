from fastapi import APIRouter
from .info_type import router as info_type_router

router = APIRouter()

router.include_router(info_type_router, prefix="/info_type")