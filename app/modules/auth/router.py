from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.modules.auth.schemas import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse,    
    )
from app.modules.auth.service import AuthService
router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    new_user = auth_service.register_user(user)
    return new_user

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    token = auth_service.login_user(user)
    return token