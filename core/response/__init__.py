from typing import Any
from core.response.schema import HZResponseMeta, HZResponseModel, Pagination


class HZResponse:
    """
    统一返回方法

    """

    @staticmethod
    async def __response(
        *, data: Any | None = None, code: str = "000000", msg: str = "请求成功"
    ) -> HZResponseMeta:
        """
        请求成功返回通用方法

        :param res: 返回信息
        :param data: 返回数据
        :return:
        """
        return HZResponseMeta(code=code, msg=msg, data=data)

    @classmethod
    async def success(cls, data: Any | None = None) -> HZResponseMeta:
        return await cls.__response(data=data)
    

__all__ = ["HZResponse", "HZResponseModel", "Pagination"]