from fastapi import FastAPI
from app.api.routes import auth, organization, project


app = FastAPI()
app.include_router(auth.router)
app.include_router(organization.router)
app.include_router(project.router)


