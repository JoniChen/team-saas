from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.api.routes import auth, organization, project
from app.core.logging import RequestIDMiddleware, setup_logging
from app.db.session import SessionLocal

setup_logging()

app = FastAPI(title="Team SaaS API")
app.add_middleware(RequestIDMiddleware)

app.include_router(auth.router)
app.include_router(organization.router)
app.include_router(project.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/health/ready")
def health_ready() -> dict:
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except OperationalError:
        raise HTTPException(status_code=503, detail="Database unavailable")
    finally:
        db.close()
