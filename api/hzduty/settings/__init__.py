from fastapi import APIRouter
from .classes import router as classes_router
from .teams import router as teams_router
router = APIRouter()

router.include_router(classes_router, prefix="/classes")
router.include_router(teams_router, prefix="/teams")