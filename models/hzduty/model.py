from typing import List, Optional

from sqlalchemy import Column, Date, ForeignKeyConstraint, Index, Integer, String, Table, Time, text
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class Events(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(255))
    time: Mapped[Optional[datetime.time]] = mapped_column(Time)


class Node(Base):
    __tablename__ = 'node'
    __table_args__ = (
        ForeignKeyConstraint(['p_id'], ['node.id'], ondelete='CASCADE', name='p_id'),
        Index('p_id', 'p_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    p_id: Mapped[Optional[int]] = mapped_column(Integer)

    p: Mapped['Node'] = relationship('Node', remote_side=[id], back_populates='p_reverse')
    p_reverse: Mapped[List['Node']] = relationship('Node', remote_side=[p_id], back_populates='p')


t_星期表 = Table(
    '星期表', Base.metadata,
    Column('星期', String(255)),
    Column('班次', String(255)),
    Column('ID', Integer),
    Index('星期', '星期')
)


class 班次表2(Base):
    __tablename__ = '班次表2'
    __table_args__ = (
        Index('班次', '班次'),
    )

    班次ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    班次: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    班次开始: Mapped[Optional[datetime.time]] = mapped_column(Time)
    班次结束: Mapped[Optional[datetime.time]] = mapped_column(Time)

    人员表: Mapped[List['人员表']] = relationship('人员表', back_populates='班次表2_')


class 班组表(Base):
    __tablename__ = '班组表'
    __table_args__ = (
        Index('值班组织', '值班组织'),
    )

    班组ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    班组名称: Mapped[Optional[str]] = mapped_column(String(255))
    值班单位: Mapped[Optional[str]] = mapped_column(String(255))
    值班组织: Mapped[Optional[str]] = mapped_column(String(255))
    值班组长: Mapped[Optional[str]] = mapped_column(String(255))
    班组成员: Mapped[Optional[str]] = mapped_column(String(255))
    值班领导: Mapped[Optional[str]] = mapped_column(String(255))

    班次表1: Mapped[List['班次表1']] = relationship('班次表1', back_populates='班组表_')
    人员表: Mapped[List['人员表']] = relationship('人员表', back_populates='班组表_')
    组织表: Mapped[List['组织表']] = relationship('组织表', back_populates='班组表_')


class 角色权限表(Base):
    __tablename__ = '角色权限表'

    角色权限: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True)

    角色表: Mapped[List['角色表']] = relationship('角色表', back_populates='角色权限表_')


class 班次表1(Base):
    __tablename__ = '班次表1'
    __table_args__ = (
        ForeignKeyConstraint(['平时_星期'], ['星期表.星期'], name='平时2'),
        ForeignKeyConstraint(['班组ID'], ['班组表.班组ID'], ondelete='CASCADE', onupdate='RESTRICT', name='班组'),
        ForeignKeyConstraint(['节假_星期'], ['星期表.星期'], name='节假2'),
        Index('平时', '平时_班次'),
        Index('平时2', '平时_星期'),
        Index('班组', '班组ID'),
        Index('节假', '节假_班次'),
        Index('节假2', '节假_星期')
    )

    班次表1ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    班组ID: Mapped[Optional[int]] = mapped_column(Integer)
    平时_班次: Mapped[Optional[str]] = mapped_column(String(255))
    平时_星期: Mapped[Optional[str]] = mapped_column(String(255))
    节假_班次: Mapped[Optional[str]] = mapped_column(String(255))
    节假_星期: Mapped[Optional[str]] = mapped_column(String(255))

    班组表_: Mapped['班组表'] = relationship('班组表', back_populates='班次表1')


class 角色表(Base):
    __tablename__ = '角色表'
    __table_args__ = (
        ForeignKeyConstraint(['角色权限'], ['角色权限表.角色权限'], name='角色权限'),
        Index('角色名', '角色名'),
        Index('角色权限', '角色权限')
    )

    角色ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    角色名: Mapped[str] = mapped_column(VARCHAR(255), server_default=text("''"))
    密码: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    角色权限: Mapped[Optional[str]] = mapped_column(String(255))

    角色权限表_: Mapped['角色权限表'] = relationship('角色权限表', back_populates='角色表')


class 人员表(角色表):
    __tablename__ = '人员表'
    __table_args__ = (
        ForeignKeyConstraint(['人员ID'], ['角色表.角色ID'], name='人员ID'),
        ForeignKeyConstraint(['班次ID'], ['班次表2.班次ID'], name='班次ID'),
        ForeignKeyConstraint(['班组ID'], ['班组表.班组ID'], ondelete='CASCADE', onupdate='RESTRICT', name='班组ID'),
        Index('班次ID', '班次ID'),
        Index('班组ID', '班组ID')
    )

    人员ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    班次ID: Mapped[int] = mapped_column(Integer)
    日期: Mapped[Optional[datetime.date]] = mapped_column(Date)
    上班时间: Mapped[Optional[str]] = mapped_column(String(255))
    下班时间: Mapped[Optional[str]] = mapped_column(String(255))
    班组ID: Mapped[Optional[int]] = mapped_column(Integer)

    班次表2_: Mapped['班次表2'] = relationship('班次表2', back_populates='人员表')
    班组表_: Mapped['班组表'] = relationship('班组表', back_populates='人员表')


class 组织表(角色表):
    __tablename__ = '组织表'
    __table_args__ = (
        ForeignKeyConstraint(['班组ID'], ['班组表.班组ID'], ondelete='CASCADE', onupdate='RESTRICT', name='qq班组id'),
        ForeignKeyConstraint(['组织名称'], ['角色表.角色名'], name='成员名'),
        Index('班组成员ID', '班组ID'),
        Index('组织名称', '组织成员')
    )

    组织名称: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True, server_default=text("''"))
    组织成员: Mapped[str] = mapped_column(VARCHAR(255))
    值班单位: Mapped[str] = mapped_column(VARCHAR(255))
    班组ID: Mapped[Optional[int]] = mapped_column(Integer)

    班组表_: Mapped['班组表'] = relationship('班组表', back_populates='组织表')
