from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from mini_crm.models.base import Base


class LeadModel(Base):
    __tablename__ = 'leads'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True) 
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False) #external id
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)