from pydantic import BaseModel, field_validator

class CreateAccount(BaseModel):
    email: str
    password: str
    role_id: int

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

    @field_validator('password')
    def password_complexity_check(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
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