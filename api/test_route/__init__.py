from fastapi import APIRouter
from .error_route import router as test_error_router

router = APIRouter()

router.include_router(test_error_router, prefix="/error")