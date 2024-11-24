from pydantic import BaseModel, Field
from typing import Optional

class UserModel(BaseModel):
    """Class representing a user."""
    id:Optional[int] = None
    username:str
    password:str

