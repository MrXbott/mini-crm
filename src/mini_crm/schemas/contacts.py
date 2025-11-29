from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class ContactCreateData(BaseModel):
    source_id: int
    lead_email: str
    lead_first_name: Optional[str] = None
    lead_last_name: Optional[str] = None

class ContactFromDB(BaseModel):
    id: int
    source_id: int
    lead_id: int
    status: str
    created_at: datetime
    operator_id: Optional[int]

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
    