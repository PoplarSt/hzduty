from fastapi import APIRouter
from .classes import router as classes_router
from .teams import router as teams_router
# from .test_tree import router as test_tree_router321
from .TTest import router as TTest_router
from .auth import router as auth_router
router = APIRouter()

router.include_router(classes_router, prefix="/classes")
router.include_router(teams_router, prefix="/teams")
# router.include_router(test_tree_router321, prefix="/test_tree")
router.include_router(auth_router, prefix="/auth")
router.include_router(TTest_router, prefix="/TTest")