from fastapi import FastAPI
from .model import ItemModel
from ..database.database import * 

app = FastAPI()

# Debugging print to see if items are getting appended
@app.get("/", response_model=list[ItemModel])
async def get_items():
    return read()

@app.post("/", response_model=ItemModel)
def create_item(item: ItemModel):
    return create(item)
    
@app.put("/{item_id}")
def update_item(): 
    ...

@app.delete("/{item_id}", response_model=None)
def delete_item(item_id:int): 
    delete(item_id)


# create_item(ItemModel(name="Cheese Pizza", amount=1, expDate="2024/10/23"))
# delete_item(2)