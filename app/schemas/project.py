from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str


class ProjectRead(BaseModel):
    id: str
    name: str
    organization_id: str

    class Config:
        from_attributes = True
