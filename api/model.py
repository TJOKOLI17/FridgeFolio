from pydantic import BaseModel

class Item(BaseModel):
    name:str
    amount:int
    expiration_date:str

