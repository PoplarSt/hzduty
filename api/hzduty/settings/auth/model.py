from typing import List, Optional

from sqlalchemy import ForeignKeyConstraint, Index, Integer, String, Table, Time, text
from sqlalchemy.dialects.mysql import ENUM, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


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
class 组织(Base):
    __tablename__ = '组织'
    __table_args__ = (
        ForeignKeyConstraint(['用户ID'], ['login.用户ID'], ondelete='CASCADE', onupdate='CASCADE', name='LOGIN'),
        ForeignKeyConstraint(['行政区划ID'], ['行政区划.行政区划'], ondelete='CASCADE', onupdate='CASCADE', name='行政区划ID'),
        Index('LOGIN', '用户ID'),
        Index('行政区划ID', '行政区划ID')
    )

    组织ID:Mapped[int] = mapped_column(Integer, primary_key=True)
    组织名称: Mapped[Optional[str]] = mapped_column(String(255))
    行政区划ID: Mapped[Optional[str]] = mapped_column(String(255))
    用户ID: Mapped[Optional[int]] = mapped_column(Integer)

    login: Mapped['Login'] = relationship('Login', back_populates='组织')
    行政区划_: Mapped['行政区划'] = relationship('行政区划', back_populates='组织')
class 行政区划(Base):
    __tablename__ = '行政区划'

    行政区划: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True)

    # 人: Mapped[List['人']] = relationship('人', back_populates='行政区划1')
    # 班次类型: Mapped[List['班次类型']] = relationship('班次类型', back_populates='行政区划1')
    # 班组: Mapped[List['班组']] = relationship('班组', back_populates='行政区划1')
    组织: Mapped[List['组织']] = relationship('组织', back_populates='行政区划_')
