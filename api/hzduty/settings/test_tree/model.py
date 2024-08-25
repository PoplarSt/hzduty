from typing import List, Optional

from sqlalchemy import ForeignKeyConstraint, Index, Integer
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Node(Base):
    __tablename__ = 'node'
    __table_args__ = (
        ForeignKeyConstraint(['p_id'], ['node.id'], ondelete='CASCADE', name='p_id'),
        Index('p_id', 'p_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    p_id: Mapped[Optional[int]] = mapped_column(Integer)

    p: Mapped['Node'] = relationship('Node', remote_side=[id], back_populates='children')
    children: Mapped[List['Node']] = relationship('Node', remote_side=[p_id], back_populates='p')
