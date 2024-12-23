from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.deps import get_db, create_access_token, get_current_user
from app.models.user import User
from app.schemas.user import (
    UserCreate, User as UserSchema, Token, PasswordReset,
    EmailVerify, ChangePassword
)
from passlib.context import CryptContext
import secrets
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def generate_token() -> str:
    return secrets.token_urlsafe(32)

def send_verification_email(email: str, token: str):
    """
    In a production environment, this would send an actual email.
    For now, we just log it.
    """
    logger.info(f"Verification email would be sent to {email} with token {token}")

def send_password_reset_email(email: str, token: str):
    """
    In a production environment, this would send an actual email.
    For now, we just log it.
    """
    logger.info(f"Password reset email would be sent to {email} with token {token}")

@router.post("/register", response_model=UserSchema)
def register(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    background_tasks: BackgroundTasks
):
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    verification_token = generate_token()
    user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        verification_token=verification_token,
        is_active=False  # User starts as inactive until email is verified
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Send verification email in background
    background_tasks.add_task(send_verification_email, user.email, verification_token)
    
    return user

@router.post("/login", response_model=Token)
def login(
    *,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please verify your email before logging in",
        )
    
    # Update last login timestamp
    user.last_login = datetime.utcnow()
    db.commit()
    
    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
    }

@router.post("/verify-email")
def verify_email(*, db: Session = Depends(get_db), verify_data: EmailVerify):
    user = db.query(User).filter(
        User.email == verify_data.email,
        User.verification_token == verify_data.token
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Invalid verification token",
        )
    
    user.is_active = True
    user.verification_token = None
    user.email_verified_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Email verified successfully"}

@router.post("/forgot-password")
def forgot_password(
    *,
    db: Session = Depends(get_db),
    email: str,
    background_tasks: BackgroundTasks
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        # Don't reveal whether the email exists
        return {"message": "If the email exists, a password reset link will be sent"}
    
    reset_token = generate_token()
    user.reset_token = reset_token
    user.reset_token_expires = datetime.utcnow() + timedelta(hours=24)
    db.commit()
    
    # Send password reset email in background
    background_tasks.add_task(send_password_reset_email, email, reset_token)
    
    return {"message": "If the email exists, a password reset link will be sent"}

@router.post("/reset-password")
def reset_password(*, db: Session = Depends(get_db), reset_data: PasswordReset):
    user = db.query(User).filter(
        User.email == reset_data.email,
        User.reset_token == reset_data.token
    ).first()
    
    if not user or not user.reset_token_expires or user.reset_token_expires < datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset token",
        )
    
    user.hashed_password = get_password_hash(reset_data.new_password)
    user.reset_token = None
    user.reset_token_expires = None
    user.password_changed_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Password reset successfully"}

@router.get("/me", response_model=UserSchema)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/change-password")
def change_password(
    *,
    db: Session = Depends(get_db),
    password_data: ChangePassword,
    current_user: User = Depends(get_current_user)
):
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect password",
        )
    
    current_user.hashed_password = get_password_hash(password_data.new_password)
    current_user.password_changed_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Password changed successfully"}
