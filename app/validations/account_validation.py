from pydantic import BaseModel, EmailStr, field_validator
class CreateAccount(BaseModel):
    email: EmailStr
    password: str
    role_id: int

    @field_validator('email')
    def email_must_be_provided(cls, v):
        if not v:
            raise ValueError('Email must be provided')
        return v
    
    @field_validator('email')
    def email_complexity_check(cls, v):
        if len(v) < 12:
            raise ValueError('email must be at least 12 characters')
        if len(v) > 50:
            raise ValueError('Email must not exceed 50 characters')
        if '@' not in v or '.' not in v:
            raise ValueError('Email must contain "@" and "." characters')
        return v

    @field_validator('email')
    def email_complexity_check(cls, v):
        if len(v) < 12:
            raise ValueError('email must be at least 12 characters')
        if len(v) > 50:
            raise ValueError('Email must not exceed 50 characters')
        if '@' not in v or '.' not in v:
            raise ValueError('Email must contain "@" and "." characters')
        return v

    @field_validator('password')
    def password_must_be_provided(cls, v):
        if not v:
            raise ValueError('Password must be provided')
        return v

    @field_validator('password')
    def password_complexity_check(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain small character at least one lowercase letter')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain upper character at least one uppercase letter')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain number at least one digit')
        return v
    
    @field_validator('role_id')
    def role_id_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Role ID must be a positive integer')
        return v

class LoginAccount(BaseModel):
    email: EmailStr
    password: str

    @field_validator('email')
    def email_must_be_provided(cls, v):
        if not v:
            raise ValueError('Email must be provided')
        return v

    @field_validator('password')
    def password_must_be_provided(cls, v):
        if not v:
            raise ValueError('Password must be provided')
        return v
    
