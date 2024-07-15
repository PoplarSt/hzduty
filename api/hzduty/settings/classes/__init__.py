from fastapi import APIRouter
from .views import router as classes_router

router = APIRouter()

router.include_router(classes_router)