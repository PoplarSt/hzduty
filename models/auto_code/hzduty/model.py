from typing import List, Optional

from sqlalchemy import ForeignKeyConstraint, Index, Integer, String
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class 行政区划(Base):
    __tablename__ = '行政区划'

    行政区划: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True)

    班组: Mapped[List['班组']] = relationship('班组', back_populates='行政区划1')


class 班组(Base):
    __tablename__ = '班组'
    __table_args__ = (
        ForeignKeyConstraint(['行政区划'], ['行政区划.行政区划'], ondelete='CASCADE', onupdate='CASCADE', name='班组行政区划'),
        Index('班组行政区划', '行政区划')
    )

    值班班组ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    值班单位: Mapped[Optional[str]] = mapped_column(String(255))
    序号: Mapped[Optional[str]] = mapped_column(String(255))
    班组名称: Mapped[Optional[str]] = mapped_column(String(255))
    行政区划_: Mapped[Optional[str]] = mapped_column('行政区划', String(255))

    行政区划1: Mapped['行政区划'] = relationship('行政区划', back_populates='班组')
