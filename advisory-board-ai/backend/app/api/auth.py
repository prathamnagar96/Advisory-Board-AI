from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.utils.security import (
    verify_password,
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user,
)

router = APIRouter()
security = HTTPBearer()

# Pydantic models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

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

# Mock user database for demo - in real app, this would be actual DB queries
mock_users = {}

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserRegister):
    """
    Register a new user.
    """
    # Check if user already exists
    if user.username in mock_users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Hash password
    hashed_password = get_password_hash(user.password)

    # Create user (in real app, this would save to database)
    user_id = len(mock_users) + 1
    new_user = {
        "id": user_id,
        "email": user.email,
        "username": user.username,
        "hashed_password": hashed_password,
        "full_name": user.full_name,
        "is_active": True,
        "created_at": datetime.utcnow()
    }

    mock_users[user.username] = new_user

    return UserResponse(
        id=new_user["id"],
        email=new_user["email"],
        username=new_user["username"],
        full_name=new_user["full_name"],
        is_active=new_user["is_active"],
        created_at=new_user["created_at"]
    )

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: UserLogin):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = authenticate_user(mock_users, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user["id"])}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(verify_token)):
    """
    Get current user.
    """
    user_id = int(current_user.get("sub"))
    # In real app, fetch from database
    # For demo, find in mock users
    user = None
    for u in mock_users.values():
        if u["id"] == user_id:
            user = u
            break

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(
        id=user["id"],
        email=user["email"],
        username=user["username"],
        full_name=user["full_name"],
        is_active=user["is_active"],
        created_at=user["created_at"]
    )

# Helper function for mock authentication
def authenticate_user(users_dict: dict, username: str, password: str):
    """
    Authenticate user with username/email and password.
    """
    user = users_dict.get(username)
    if not user:
        # Also check by email
        for u in users_dict.values():
            if u["email"] == username:
                user = u
                break

    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user