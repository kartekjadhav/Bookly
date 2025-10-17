from pydantic import BaseModel, Field, EmailStr
from uuid import uuid4, UUID
from datetime import datetime

class UserModel(BaseModel):
    uid: UUID
    username: str
    first_name: str
    last_name: str
    email: str
    verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime

class UserCreateModel(BaseModel):
    username: str = Field(max_length=50)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=100)
    password: str = Field(min_length=6, max_length=100, exclude=True)
    is_verified: bool = Field(default=False)

class UserLoginModel(BaseModel):
    email: EmailStr = Field(min_length=6)
    password: str = Field(min_length=6, exclude=True)