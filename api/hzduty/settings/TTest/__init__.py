from fastapi import APIRouter
from .router import router as  r1
router = APIRouter()
router.include_router(r1)