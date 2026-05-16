from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectRead
from app.api.deps import get_db
from app.core.security import get_current_user

router = APIRouter(prefix="/projects")


@router.post("/", response_model=ProjectRead)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.organization_id is None:
        raise HTTPException(
            status_code=400,
            detail="User must belong to an organization before creating projects",
        )
    new_project = Project(
        name=project.name,
        organization_id=current_user.organization_id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


@router.get("/", response_model=list[ProjectRead])
def list_projects(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.organization_id is None:
        raise HTTPException(
            status_code=400,
            detail="User must belong to an organization before listing projects",
        )
    projects = db.query(Project).filter(
        Project.organization_id == current_user.organization_id
    ).all()

    return projects
