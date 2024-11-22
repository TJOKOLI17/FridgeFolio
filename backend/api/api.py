from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .model import ItemModel
from ..database.database import * 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust the origin as necessary
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/", response_model=list[ItemModel], tags=["Item"])
async def get_items():
    return read()

#thrown away page
@app.get("/deleted", response_model=list[ItemModel], tags=["Item"])
async def get_deleted_items():
    deleted_items:list[ItemModel] = read_deleted()
    # if deleted_items is None:
    #     raise HTTPException(status_code=404, detail={"message": "Items not found"})
    return deleted_items

@app.get("/{item_id}", response_model=ItemModel, tags=["Item"])
async def get_item_by_id(item_id:int):
    item = read_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail={"id": item_id, "message": "Item not found"})
    return read_by_id(item_id)

@app.post("/", response_model=ItemModel, tags=["Item"])
def create_item(item: ItemModel):
    return create(item)
    
@app.put("/", response_model=None, tags=["Item"])
def update_item(item: ItemModel): 
    updated_item:ItemModel = update(item.id, item.amount)
    if updated_item is None:
        raise HTTPException(status_code=404, detail={"id": item.id, "message": "Item not found"})

@app.delete("/{item_id}", response_model=None, tags=["Item"])
def delete_item(item_id:int): 
    delete(item_id)