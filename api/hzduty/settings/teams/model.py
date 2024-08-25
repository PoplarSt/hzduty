from typing import List, Optional

from sqlalchemy import Column, Date, ForeignKeyConstraint, Index, Integer, String, Table, Time, text
from sqlalchemy.dialects.mysql import ENUM, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime


class Base(DeclarativeBase):
    pass


class 行政区划(Base):
    __tablename__ = '行政区划'

    行政区划: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True)

    人: Mapped[List['人']] = relationship('人', back_populates='行政区划1')
    班组: Mapped[List['班组']] = relationship('班组', back_populates='行政区划1')


class 人(Base):
    __tablename__ = '人'
    __table_args__ = (
        ForeignKeyConstraint(['行政区划'], ['行政区划.行政区划'], ondelete='RESTRICT', onupdate='RESTRICT',
                             name='行政区划'),
        Index('人员', '人员'),
        Index('行政区划', '行政区划')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    人员: Mapped[Optional[str]] = mapped_column(String(255))
    行政区划_: Mapped[Optional[str]] = mapped_column('行政区划', String(255))
    行政区划1: Mapped['行政区划'] = relationship('行政区划', back_populates='人')
    排班成员班组成员: Mapped[List['排班成员班组成员']] = relationship('排班成员班组成员', back_populates='user')
    组长领导: Mapped[List['组长领导']] = relationship('组长领导', back_populates='user')
class 排班成员班组成员(Base):
    __tablename__ = '排班成员班组成员'
    __table_args__ = (
        ForeignKeyConstraint(['duty_group_id'], ['班组.值班班组ID'], ondelete='CASCADE', onupdate='CASCADE',
                             name='dgi1'),
        ForeignKeyConstraint(['user_id'], ['人.id'], ondelete='CASCADE', onupdate='CASCADE', name='uid1'),
        Index('dgi1', 'duty_group_id'),
        Index('uid1', 'user_id')
    )

    member_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    duty_group_id: Mapped[Optional[int]] = mapped_column(Integer)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    姓名: Mapped[Optional[str]] = mapped_column(String(255))


    duty_group: Mapped['班组'] = relationship('班组', back_populates='排班成员班组成员')
    user: Mapped['人'] = relationship('人', back_populates='排班成员班组成员')
class 组长领导(Base):
    __tablename__ = '组长领导'
    __table_args__ = (
        ForeignKeyConstraint(['duty_group_id'], ['班组.值班班组ID'], ondelete='CASCADE', onupdate='CASCADE', name='dgi'),
        ForeignKeyConstraint(['user_id'], ['人.id'], ondelete='CASCADE', onupdate='CASCADE', name='uid'),
        Index('dgi', 'duty_group_id'),
        Index('uid', 'user_id')
    )

    duty_leader_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    duty_group_id: Mapped[Optional[int]] = mapped_column(Integer)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    姓名:Mapped[Optional[str]] = mapped_column(String(255))
    type: Mapped[Optional[int]] = mapped_column(Integer)

    duty_group: Mapped['班组'] = relationship('班组', back_populates='组长领导')
    user: Mapped['人'] = relationship('人', back_populates='组长领导')

class 班组(Base):
    __tablename__ = '班组'
    __table_args__ = (
        ForeignKeyConstraint(['行政区划'], ['行政区划.行政区划'], ondelete='CASCADE', onupdate='CASCADE',
                             name='班组行政区划'),
        Index('班组行政区划', '行政区划')
    )

    值班班组ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    值班单位: Mapped[Optional[str]] = mapped_column(String(255))
    序号: Mapped[Optional[str]] = mapped_column(String(255))
    班组名称: Mapped[Optional[str]] = mapped_column(String(255))
    行政区划: Mapped[Optional[str]] = mapped_column('行政区划', String(255))

    行政区划1: Mapped['行政区划'] = relationship('行政区划', back_populates='班组')
    排班成员班组成员: Mapped[List['排班成员班组成员']] = relationship('排班成员班组成员', back_populates='duty_group')
    组长领导: Mapped[List['组长领导']] = relationship('组长领导', back_populates='duty_group')




