from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from mini_crm.models.base import Base

if TYPE_CHECKING:
    from mini_crm.models.operators import OperatorModel
    from mini_crm.models.sources_operators import SourceOperatorModel

class SourceModel(Base):
    __tablename__ = 'sources'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True) 
    name: Mapped[str] = mapped_column(String, nullable=False)

    operators_assoc: Mapped[list['SourceOperatorModel']] = relationship(back_populates='source', cascade='all, delete-orphan')

    operators: Mapped[list['OperatorModel']] = relationship(secondary='sources_operators', viewonly=True)


