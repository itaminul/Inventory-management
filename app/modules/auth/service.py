from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import logging
from app.modules.auth.repository import AuthRepository  
logger = logging.getLogger(__name__)        
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

class AuthService:
    
    def __init__(self, db: Session):
        self.auth_repository = AuthRepository(db)
        
    def register_user(self, data):
        
        existing_user = self.auth_repository.get_user_by_username(data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        
        hashed_password = hash_password(data.password)
        new_user = self.auth_repository.create_user(
            username=data.username,
            email=data.email,
            hashed_password=hashed_password
        )
        return new_user    
    
    def login_user(self, data):
        if data.email is not None:
            user = self.auth_repository.get_user_by_email(data.email)
        elif data.username is not None:
            user = self.auth_repository.get_user_by_username(data.username)
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Either username or email is required",
            )

        logger.info("Login attempt")
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        access_token = create_access_token({"sub": user.username})
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        return {"access_token": access_token, "token_type": "bearer"}