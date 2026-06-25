from typing import cast

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import create_access_token, get_current_user, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import TokenResponse
from app.schemas.user import UserCreate, UserLogin

router = APIRouter(prefix="/auth")


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)) -> dict:
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = User(
        email=user.email,
        password_hash=hash_password(user.password)
    )
    db.add(db_user)
    db.flush()
    return {"message": "User created"}


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)) -> dict:
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, cast(str, db_user.password_hash)):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": str(db_user.id)})
    return {"access_token": token}


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)) -> dict:
    return {
        "id": str(current_user.id),
        "email": current_user.email,
    }