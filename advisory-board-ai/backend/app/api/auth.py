from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.utils.security import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user,
)

router = APIRouter()
security = HTTPBearer()


class Token(BaseModel):
    access_token: str
    token_type: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserRegister(BaseModel):
    email: str
    username: str
    password: str
    full_name: str | None = None


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str | None = None
    is_active: bool
    created_at: datetime


@router.post("/register", response_model=UserResponse)
async def register_user(user: UserRegister, db: Session = Depends(get_db)):
    """Register a new user in the database."""
    existing = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered",
        )

    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name,
        is_active=True,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserResponse(
        id=db_user.id,
        email=db_user.email,
        username=db_user.username,
        full_name=db_user.full_name,
        is_active=db_user.is_active,
        created_at=db_user.created_at,
    )


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: UserLogin, db: Session = Depends(get_db)):
    """Issue a JWT for valid email/username + password."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Return the currently authenticated user."""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
    )
