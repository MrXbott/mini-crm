from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from mini_crm.models.base import Base

if TYPE_CHECKING:
    from mini_crm.models.sources import SourceModel
    from mini_crm.models.sources_operators import SourceOperatorModel

class OperatorModel(Base):
    __tablename__ = 'operators'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True) 
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    max_capacity: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    current_capacity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    sources_assoc: Mapped[list['SourceOperatorModel']] = relationship(back_populates='operator', cascade='all, delete-orphan')

    sources: Mapped[list['SourceModel']] = relationship(secondary='sources_operators', viewonly=True)