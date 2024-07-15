from fastapi import APIRouter
from .database import router as database_router
from .schema import router as schema_router
router = APIRouter()

router.include_router(database_router, prefix="/database")
router.include_router(schema_router, prefix="/schema")