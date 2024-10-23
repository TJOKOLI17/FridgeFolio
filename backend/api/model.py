from pydantic import BaseModel
from typing import Optional

class ItemModel(BaseModel):
    """Class representing each fridge item."""
    id:Optional[int] = None
    name:str
    amount:int
    expDate:str

