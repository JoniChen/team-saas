import uuid

from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    name: str


class ProjectRead(BaseModel):
    id: uuid.UUID
    name: str
    organization_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
