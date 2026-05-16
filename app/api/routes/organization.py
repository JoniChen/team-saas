from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.organization import OrganizationCreate, OrganizationRead
from app.models.organization import Organization
from app.api.deps import get_db
from app.core.security import get_current_user

router = APIRouter(prefix="/organizations")

@router.post("/", response_model=OrganizationRead)
def create_organization(
    org: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    existing = db.query(Organization).filter(Organization.name == org.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Organization already exists")

    new_org = Organization(name=org.name)
    db.add(new_org)
    db.commit()
    db.refresh(new_org)

    # Assign current user to this organization
    current_user.organization_id = new_org.id
    db.commit()
    db.refresh(current_user)

    return new_org
