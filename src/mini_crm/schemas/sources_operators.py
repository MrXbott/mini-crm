from pydantic import BaseModel, Field, ConfigDict

class SourceOperatorData(BaseModel):
    operator_id: int
    weight: int = Field(ge=0)

class SourceOperatorFromDB(BaseModel):
    source_id: int
    operator_id: int
    weight: int 

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)