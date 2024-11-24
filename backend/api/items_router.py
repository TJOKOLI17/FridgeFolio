from fastapi import APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models.ItemModel import ItemModel
from ..database.items_database import * 

router = APIRouter(
    prefix="/items",  # All routes will have this prefix
    tags=["Item"],    # Tag for documentation purposes
)

@router.get("/", response_model=list[ItemModel])
async def get_items():
    return read_item()

@router.get("/deleted", response_model=list[ItemModel])
async def get_deleted_items():
    deleted_items: list[ItemModel] = read_deleted_items()
    return deleted_items

@router.get("/{item_id}", response_model=ItemModel)
async def get_item_by_id(item_id: int):
    item = read_item_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail={"id": item_id, "message": "Item not found"})
    return item

@router.post("/", response_model=ItemModel)
async def create_new_item(item: ItemModel):
    return create_item(item)

@router.put("/", response_model=None)
async def update_item(item: ItemModel): 
    updated_item: ItemModel = update_item(item.id, item.amount)
    if updated_item is None:
        raise HTTPException(status_code=404, detail={"id": item.id, "message": "Item not found"})
    return updated_item

@router.delete("/{item_id}", response_model=None)
async def delete_existing_item(item_id: int): 
    item = read_item_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail={"id": item_id, "message": "Item not found"})
    delete_item(item_id)