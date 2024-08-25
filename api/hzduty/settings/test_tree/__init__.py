import pymysql
pymysql.install_as_MySQLdb()
from fastapi import APIRouter
from .views import router as test_router123

router = APIRouter()
router.include_router(test_router123)