from fastapi import APIRouter

from api.test_route.error_route.interface import TestParams


router = APIRouter(tags=["参数"])




@router.post(
    "/",
    summary="测试post参数错误",
    description="测试参数错误接口，这里是详细信息",
)
async def test_check_params(schema: TestParams) -> TestParams:
    """
    测试参数错误接口，这里是详细信息,支持markdown
    """
    return schema


@router.get(
    "/query",
    summary="测试query参数错误",
    description="测试参数错误接口，这里是详细信息",
)
async def test_check_params2(name: str, password: str) -> TestParams:
    """
    测试参数错误接口，这里是详细信息,支持markdown
    """
    return TestParams(姓名=name, 密码=password)