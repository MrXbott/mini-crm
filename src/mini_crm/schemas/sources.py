from pydantic import BaseModel, Field, ConfigDict


class SourceCreateData(BaseModel):
    name: str

class SourceFromDB(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)