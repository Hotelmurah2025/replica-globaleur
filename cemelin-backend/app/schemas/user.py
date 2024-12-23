from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: constr(min_length=8)  # Minimum 8 characters for password

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    email_verified_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    password_changed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None

class PasswordReset(BaseModel):
    email: EmailStr
    token: str
    new_password: constr(min_length=8)

class EmailVerify(BaseModel):
    email: EmailStr
    token: str

class ChangePassword(BaseModel):
    current_password: str
    new_password: constr(min_length=8)
