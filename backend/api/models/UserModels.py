from pydantic import BaseModel, Field
# from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Shared attributes of a user."""
    username:str

class UserCreate(UserBase):
    """Attributes required for creating a new User."""
    password: str # = Field(..., min_length=8, title="Password", description="Password must be at least 8 characters long")

class UserResponse(UserBase):
    """Attributes returned when a User is retrieved."""
    uid: int
    CreatedAt: datetime

# class Config:
#         orm_mode = True

