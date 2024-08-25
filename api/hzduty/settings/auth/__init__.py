from fastapi import APIRouter
from .views import router as login_router

router = APIRouter()

router.include_router(login_router)