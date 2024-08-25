from typing import List, Optional

from sqlalchemy import Column, Date, ForeignKeyConstraint, Index, Integer, String, Table, Time, text
from sqlalchemy.dialects.mysql import ENUM, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class Login(Base):
    __tablename__ = 'login'

    用户ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    用户编号: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    账号: Mapped[Optional[str]] = mapped_column(String(255))
    密码: Mapped[Optional[str]] = mapped_column(String(255))
    姓名: Mapped[Optional[str]] = mapped_column(String(255))
    用户类别ID: Mapped[Optional[int]] = mapped_column(Integer)
    联系电话: Mapped[Optional[str]] = mapped_column(String(255))
    邮箱地址: Mapped[Optional[str]] = mapped_column(String(255))

    组织: Mapped[List['组织']] = relationship('组织', back_populates='login')
    角色: Mapped[List['角色']] = relationship('角色', back_populates='login')


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


t_星期表f = Table(
    '星期表f', Base.metadata,
    Column('星期', String(255)),
    Column('班次', String(255)),
    Column('ID', Integer),
    Index('星期', '星期')
)


class 班次表2f(Base):
    __tablename__ = '班次表2f'
    __table_args__ = (
        Index('aa', 'aa'),
        Index('班次', '班次')
    )

    班次ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    班次: Mapped[Optional[str]] = mapped_column(VARCHAR(20))
    班次开始: Mapped[Optional[datetime.time]] = mapped_column(Time)
    班次结束: Mapped[Optional[datetime.time]] = mapped_column(Time)
    TYPE: Mapped[Optional[str]] = mapped_column(ENUM('normal', 'holiday'))
    aa: Mapped[Optional[str]] = mapped_column(String(255))

    人员表f: Mapped[List['人员表f']] = relationship('人员表f', back_populates='班次表2f_')


class 班组表f(Base):
    __tablename__ = '班组表f'
    __table_args__ = (
        Index('值班组织', '值班单位'),
    )

    班组ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    班组名称: Mapped[Optional[str]] = mapped_column(String(255))
    值班领导: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    值班单位: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    值班组长: Mapped[Optional[str]] = mapped_column(String(255))
    班组成员: Mapped[Optional[str]] = mapped_column(String(255))

    班次表1f: Mapped[List['班次表1f']] = relationship('班次表1f', back_populates='班组表f_')
    人员表f: Mapped[List['人员表f']] = relationship('人员表f', back_populates='班组表f_')
    组织表f: Mapped[List['组织表f']] = relationship('组织表f', back_populates='班组表f_')


class 行政区划(Base):
    __tablename__ = '行政区划'

    行政区划: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True)

    人: Mapped[List['人']] = relationship('人', back_populates='行政区划1')
    班次类型: Mapped[List['班次类型']] = relationship('班次类型', back_populates='行政区划1')
    班组: Mapped[List['班组']] = relationship('班组', back_populates='行政区划1')
    组织: Mapped[List['组织']] = relationship('组织', back_populates='行政区划_')


class 角色权限表(Base):
    __tablename__ = '角色权限表'

    角色权限: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True)
    行政区划_: Mapped[Optional[str]] = mapped_column('行政区划', String(255))

    角色表: Mapped[List['角色表']] = relationship('角色表', back_populates='角色权限表_')


class 人(Base):
    __tablename__ = '人'
    __table_args__ = (
        ForeignKeyConstraint(['行政区划'], ['行政区划.行政区划'], ondelete='RESTRICT', onupdate='RESTRICT', name='行政区划'),
        Index('人员', '人员'),
        Index('行政区划', '行政区划')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    人员: Mapped[Optional[str]] = mapped_column(String(255))
    行政区划_: Mapped[Optional[str]] = mapped_column('行政区划', String(255))

    行政区划1: Mapped['行政区划'] = relationship('行政区划', back_populates='人')
    排班成员班组成员: Mapped[List['排班成员班组成员']] = relationship('排班成员班组成员', back_populates='user')
    组长领导: Mapped[List['组长领导']] = relationship('组长领导', back_populates='user')


class 班次类型(Base):
    __tablename__ = '班次类型'
    __table_args__ = (
        ForeignKeyConstraint(['行政区划'], ['行政区划.行政区划'], name='行政区划1'),
        Index('班次类型', '值班班次类型'),
        Index('行政区划1', '行政区划')
    )

    值班班次类型: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True)
    值班班次类型ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    可删除: Mapped[Optional[int]] = mapped_column(Integer)
    行政区划_: Mapped[Optional[str]] = mapped_column('行政区划', String(255))

    行政区划1: Mapped['行政区划'] = relationship('行政区划', back_populates='班次类型')
    班次: Mapped[List['班次']] = relationship('班次', foreign_keys='[班次.type]', back_populates='班次类型_')
    班次_: Mapped[List['班次']] = relationship('班次', foreign_keys='[班次.type_name]', back_populates='班次类型1')


class 班次表1f(Base):
    __tablename__ = '班次表1f'
    __table_args__ = (
        ForeignKeyConstraint(['平时_星期'], ['星期表f.星期'], name='平时2'),
        ForeignKeyConstraint(['班组ID'], ['班组表f.班组ID'], ondelete='CASCADE', onupdate='RESTRICT', name='班组'),
        ForeignKeyConstraint(['节假_星期'], ['星期表f.星期'], name='节假2'),
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

    班组表f_: Mapped['班组表f'] = relationship('班组表f', back_populates='班次表1f')


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
    排班成员班组成员: Mapped[List['排班成员班组成员']] = relationship('排班成员班组成员', back_populates='duty_group')
    组长领导: Mapped[List['组长领导']] = relationship('组长领导', back_populates='duty_group')


class 组织(Base):
    __tablename__ = '组织'
    __table_args__ = (
        ForeignKeyConstraint(['用户ID'], ['login.用户ID'], ondelete='CASCADE', onupdate='CASCADE', name='LOGIN'),
        ForeignKeyConstraint(['行政区划ID'], ['行政区划.行政区划'], ondelete='CASCADE', onupdate='CASCADE', name='行政区划ID'),
        Index('LOGIN', '用户ID'),
        Index('行政区划ID', '行政区划ID')
    )

    组织ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    组织名称: Mapped[Optional[str]] = mapped_column(String(255))
    行政区划ID: Mapped[Optional[str]] = mapped_column(String(255))
    用户ID: Mapped[Optional[int]] = mapped_column(Integer)

    login: Mapped['Login'] = relationship('Login', back_populates='组织')
    行政区划_: Mapped['行政区划'] = relationship('行政区划', back_populates='组织')


class 角色(Base):
    __tablename__ = '角色'
    __table_args__ = (
        ForeignKeyConstraint(['用户ID'], ['login.用户ID'], ondelete='CASCADE', onupdate='CASCADE', name='LOGIN1'),
        Index('LOGIN1', '用户ID')
    )

    角色ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    角色名称: Mapped[Optional[str]] = mapped_column(String(255))
    角色描述: Mapped[Optional[str]] = mapped_column(String(255))
    角色标识: Mapped[Optional[str]] = mapped_column(String(255))
    用户ID: Mapped[Optional[int]] = mapped_column(Integer)

    login: Mapped['Login'] = relationship('Login', back_populates='角色')


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
    所属行政区: Mapped[Optional[str]] = mapped_column(String(255))

    角色权限表_: Mapped['角色权限表'] = relationship('角色权限表', back_populates='角色表')


class 人员表f(角色表):
    __tablename__ = '人员表f'
    __table_args__ = (
        ForeignKeyConstraint(['人员ID'], ['角色表.角色ID'], name='人员ID'),
        ForeignKeyConstraint(['班次ID'], ['班次表2f.班次ID'], ondelete='CASCADE', onupdate='RESTRICT', name='班次ID'),
        ForeignKeyConstraint(['班组ID'], ['班组表f.班组ID'], ondelete='CASCADE', onupdate='RESTRICT', name='班组ID'),
        Index('班次ID', '班次ID'),
        Index('班组ID', '班组ID')
    )

    人员ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    班次ID: Mapped[int] = mapped_column(Integer)
    日期: Mapped[Optional[datetime.date]] = mapped_column(Date)
    上班时间: Mapped[Optional[str]] = mapped_column(String(255))
    下班时间: Mapped[Optional[str]] = mapped_column(String(255))
    班组ID: Mapped[Optional[int]] = mapped_column(Integer)

    班次表2f_: Mapped['班次表2f'] = relationship('班次表2f', back_populates='人员表f')
    班组表f_: Mapped['班组表f'] = relationship('班组表f', back_populates='人员表f')


class 排班成员班组成员(Base):
    __tablename__ = '排班成员班组成员'
    __table_args__ = (
        ForeignKeyConstraint(['duty_group_id'], ['班组.值班班组ID'], ondelete='CASCADE', onupdate='CASCADE', name='dgi1'),
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


class 班次(Base):
    __tablename__ = '班次'
    __table_args__ = (
        ForeignKeyConstraint(['type'], ['班次类型.值班班次类型ID'], ondelete='CASCADE', onupdate='CASCADE', name='type'),
        ForeignKeyConstraint(['type_name'], ['班次类型.值班班次类型'], ondelete='CASCADE', onupdate='CASCADE', name='tn'),
        Index('tn', 'type_name'),
        Index('type', 'type')
    )

    值班班次ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    开始时间: Mapped[Optional[datetime.time]] = mapped_column(Time)
    班次名称: Mapped[Optional[str]] = mapped_column(String(255))
    type: Mapped[Optional[int]] = mapped_column(Integer)
    type_name: Mapped[Optional[str]] = mapped_column(String(255))

    班次类型_: Mapped['班次类型'] = relationship('班次类型', foreign_keys=[type], back_populates='班次')
    班次类型1: Mapped['班次类型'] = relationship('班次类型', foreign_keys=[type_name], back_populates='班次_')


class 组织表f(角色表):
    __tablename__ = '组织表f'
    __table_args__ = (
        ForeignKeyConstraint(['班组ID'], ['班组表f.班组ID'], ondelete='CASCADE', onupdate='RESTRICT', name='qq班组id'),
        ForeignKeyConstraint(['组织成员'], ['角色表.角色名'], name='成员名'),
        Index('班组成员ID', '班组ID'),
        Index('组织名称', '组织名称')
    )

    组织成员: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True, server_default=text("''"))
    组织名称: Mapped[str] = mapped_column(VARCHAR(255))
    值班单位: Mapped[str] = mapped_column(VARCHAR(255))
    班组ID: Mapped[Optional[int]] = mapped_column(Integer)
    岗位职责: Mapped[Optional[str]] = mapped_column(ENUM('值班组长', '班组成员'))

    班组表f_: Mapped['班组表f'] = relationship('班组表f', back_populates='组织表f')


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
    姓名: Mapped[Optional[str]] = mapped_column(String(255))
    type: Mapped[Optional[int]] = mapped_column(Integer)

    duty_group: Mapped['班组'] = relationship('班组', back_populates='组长领导')
    user: Mapped['人'] = relationship('人', back_populates='组长领导')
