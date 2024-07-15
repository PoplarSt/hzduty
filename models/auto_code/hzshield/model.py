from sqlalchemy import DateTime, ForeignKeyConstraint, Index, String, Text
from sqlalchemy.dialects.mysql import TINYINT
from typing import List, Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column, relationship
import datetime

class Base(MappedAsDataclass, DeclarativeBase):
    pass


class N01信息模板(Base):
    __tablename__ = 'n01信息模板'

    信息模板ID: Mapped[str] = mapped_column(String(32), primary_key=True)
    行政区划ID: Mapped[str] = mapped_column(String(32))
    信息模板名称: Mapped[str] = mapped_column(String(32))
    业务类型ID: Mapped[str] = mapped_column(String(32))
    信息类型ID: Mapped[str] = mapped_column(String(32))
    模板内容: Mapped[str] = mapped_column(Text)
    创建时间: Mapped[datetime.datetime] = mapped_column(DateTime)
    更新时间: Mapped[datetime.datetime] = mapped_column(DateTime)

    n11信息拟制: Mapped[List['N11信息拟制']] = relationship('N11信息拟制', back_populates='n01信息模板')


class N01信息类型(Base):
    __tablename__ = 'n01信息类型'

    信息类型ID: Mapped[str] = mapped_column(String(64), primary_key=True)
    信息类型名称: Mapped[Optional[str]] = mapped_column(String(255))
    业务类型ID: Mapped[Optional[str]] = mapped_column(String(32))
    创建时间: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    更新时间: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    描述: Mapped[Optional[str]] = mapped_column(String(2000))
    告警类型: Mapped[Optional[str]] = mapped_column(String(32))
    行政区划ID: Mapped[Optional[str]] = mapped_column(String(32))


class N11信息拟制(Base):
    __tablename__ = 'n11信息拟制'
    __table_args__ = (
        ForeignKeyConstraint(['信息模板ID'], ['n01信息模板.信息模板ID'], name='template'),
        Index('template', '信息模板ID')
    )

    信息ID: Mapped[str] = mapped_column(String(32), primary_key=True)
    组织ID: Mapped[Optional[str]] = mapped_column(String(32))
    组织名称: Mapped[Optional[str]] = mapped_column(String(255))
    信息标题: Mapped[Optional[str]] = mapped_column(String(2000))
    业务类型ID: Mapped[Optional[str]] = mapped_column(String(32))
    信息类型名称: Mapped[Optional[str]] = mapped_column(String(255))
    信息类型ID: Mapped[Optional[str]] = mapped_column(String(32))
    发布方式: Mapped[Optional[str]] = mapped_column(String(8))
    开始时间: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    结束时间: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    发布范围: Mapped[Optional[str]] = mapped_column(String(8))
    信息内容: Mapped[Optional[str]] = mapped_column(Text)
    拟制部门ID: Mapped[Optional[str]] = mapped_column(String(32))
    拟制人ID: Mapped[Optional[str]] = mapped_column(String(32))
    拟制部门名称: Mapped[Optional[str]] = mapped_column(String(255))
    拟制人名称: Mapped[Optional[str]] = mapped_column(String(255))
    审核流程ID: Mapped[Optional[str]] = mapped_column(String(32))
    发布渠道: Mapped[Optional[str]] = mapped_column(String(2000))
    状态: Mapped[Optional[str]] = mapped_column(String(32))
    创建时间: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    更新时间: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    是否归档: Mapped[Optional[int]] = mapped_column(TINYINT(4))
    归档时间: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    行政区划ID: Mapped[Optional[str]] = mapped_column(String(32))
    信息模板ID: Mapped[Optional[str]] = mapped_column(String(32))

    n01信息模板: Mapped['N01信息模板'] = relationship('N01信息模板', back_populates='n11信息拟制')
