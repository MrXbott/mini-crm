from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class OperatorCreateData(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    max_capacity: Optional[int] = Field(default=5, ge=0, le=10)  
    is_active: Optional[bool] = True

class OperatorUpdateData(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    max_capacity: Optional[int] = Field(None, ge=0, le=10)  

class OperatorFromDB(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    max_capacity: int
    is_active: bool
    current_capacity: int

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class AssignedOperatorData(BaseModel):
    operator: OperatorFromDB
    source_id: int
    weight: int
    current_capacity: int

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)