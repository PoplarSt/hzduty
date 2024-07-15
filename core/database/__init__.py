from .base import HZDB

class HZSHIELD(HZDB):
    __db_name__ = "hzshield"

class HZDUTY(HZDB):
    __db_name__ = "hzduty"

__all__ = ["HZDB", "HZSHIELD"]