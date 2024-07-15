from sqlalchemy import DateTime, String, Text
from typing import List

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime


class Base(DeclarativeBase):
    pass


class D01值班班次类型(Base):
    __tablename__ = "值班班次类型"

    值班班次类型ID: Mapped[str] = mapped_column(String(32), primary_key=True)
    值班班次类型: Mapped[str] = mapped_column(String(32))
    # 信息模板名称: Mapped[str] = mapped_column(String(32))
    # 业务类型ID: Mapped[str] = mapped_column(String(32))
    # 信息类型ID: Mapped[str] = mapped_column(String(32))
    # 模板内容: Mapped[str] = mapped_column(Text)
    # 创建时间: Mapped[datetime.datetime] = mapped_column(DateTime)
    # 更新时间: Mapped[datetime.datetime] = mapped_column(DateTime)

