from pydantic import BaseModel

class OrganizationCreate(BaseModel):
    name: str

class OrganizationRead(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True
