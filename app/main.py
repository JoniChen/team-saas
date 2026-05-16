from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
import app.models.user
import app.models.organization
import app.models.project
from app.api.routes import auth, organization, project

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(organization.router)
app.include_router(project.router)


