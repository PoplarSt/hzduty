from typing import List, Optional

from sqlalchemy import ForeignKeyConstraint, Index, Integer, String, Time
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class 班次类型(Base):
    __tablename__ = '班次类型'
    __table_args__ = (
        Index('班次类型', '值班班次类型'),
    )
    值班班次类型ID: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    值班班次类型: Mapped[str] = mapped_column(VARCHAR(255))

    可删除: Mapped[Optional[int]] = mapped_column(Integer)
    行政区划:Mapped[Optional[str]] = mapped_column(String(255))

    班次: Mapped[List['班次']] = relationship('班次', back_populates='班次类型_')


class 班次(Base):
    __tablename__ = '班次'
    __table_args__ = (
        ForeignKeyConstraint(['type'], ['班次类型.值班班次类型ID'], ondelete='CASCADE', onupdate='CASCADE', name='type'),
        Index('type', 'type')
    )

    值班班次ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    开始时间:  Mapped[Optional[datetime.time]] = mapped_column(Time)
    班次名称: Mapped[Optional[str]] = mapped_column(String(255))
    type: Mapped[Optional[int]] = mapped_column(Integer)
    type_name:Mapped[Optional[str]] = mapped_column(String(255))

    班次类型_: Mapped['班次类型'] = relationship('班次类型', back_populates='班次')
