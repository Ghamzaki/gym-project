from pydantic import BaseModel, ValidationError, field_validator
from typing import Optional
from email_validator import validate_email, EmailNotValidError


# Shared properties
class UserBase(BaseModel):
    # use a plain string for email and validate/normalize with email-validator
    email: str
    is_active: bool = True
    is_superuser: bool = False
    full_name: Optional[str] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

    @field_validator('password', mode='before')
    @classmethod
    def validate_password_length(cls, v):
        if not isinstance(v, str):
            raise ValueError('password must be a string')
        # bcrypt has a 72-byte limit; ensure password won't trigger a server error
        if len(v.encode('utf-8')) > 72:
            raise ValueError('password too long; must be <= 72 bytes')
        return v

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int

    @field_validator('email', mode='before')
    @classmethod
    def normalize_email(cls, v):
        if not isinstance(v, str):
            raise ValueError('email must be a string')
        try:
            parts = validate_email(v, check_deliverability=False)
        except EmailNotValidError as e:
            raise ValueError(f'invalid email: {e}')
        # prefer the normalized/ascii email when available
        return getattr(parts, 'normalized', None) or getattr(parts, 'email', None) or getattr(parts, 'ascii_email', None)

    class Config:
        orm_mode = True

# Additional properties to return via API
class User(UserInDBBase):
    pass

# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str