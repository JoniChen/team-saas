from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    name: str


class ProjectRead(BaseModel):
    id: str
    name: str
    organization_id: str

    model_config = ConfigDict(from_attributes=True)
