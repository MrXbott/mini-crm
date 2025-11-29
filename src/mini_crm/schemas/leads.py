from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class LeadCreateData(BaseModel):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
class LeadFromDB(BaseModel):
    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)