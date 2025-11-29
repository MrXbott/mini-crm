from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from mini_crm.models.base import Base

class ContactModel(Base):
    __tablename__ = 'contacts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lead_id: Mapped[int] = mapped_column(Integer, ForeignKey('leads.id'), nullable=False)
    source_id: Mapped[int] = mapped_column(Integer, ForeignKey('sources.id'), nullable=False)
    operator_id: Mapped[int] = mapped_column(Integer, ForeignKey('operators.id'), nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default='open')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)