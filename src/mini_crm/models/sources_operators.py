from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from mini_crm.models.base import Base

if TYPE_CHECKING:
    from mini_crm.models.sources import SourceModel
    from mini_crm.models.operators import OperatorModel

class SourceOperatorModel(Base):
    __tablename__ = 'sources_operators'

    source_id: Mapped[int] = mapped_column(ForeignKey('sources.id'), primary_key=True)
    operator_id: Mapped[int] = mapped_column(ForeignKey('operators.id'), primary_key=True)
    weight: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    source: Mapped['SourceModel'] = relationship(back_populates='operators_assoc')
    operator: Mapped['OperatorModel'] = relationship(back_populates='sources_assoc')

    __table_args__ = (UniqueConstraint('source_id', 'operator_id'),)
