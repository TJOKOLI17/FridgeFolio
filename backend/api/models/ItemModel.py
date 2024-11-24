from pydantic import BaseModel, Field
from typing import Optional

class ItemModel(BaseModel):
    """Class representing each fridge item."""
    id:Optional[int] = None
    # uid:Optional[int] = None
    name:str
    amount:int = Field(..., ge=0)
    expDate:str

