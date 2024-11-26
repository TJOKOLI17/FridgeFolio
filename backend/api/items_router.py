from fastapi import APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models.ItemModel import ItemModel
from ..database.items_database import * 

router = APIRouter(
    prefix="/items",  # All routes will have this prefix
    tags=["Item"],    # Tag for documentation purposes
)

@router.get("/", response_model=list[ItemModel])
async def get_all_items():
    return read_items()

@router.get("/deleted", response_model=list[ItemModel])
async def get_all_deleted_items():
    deleted_items: list[ItemModel] = read_deleted_items()
    return deleted_items

@router.get("/{user_id}", response_model=list[ItemModel])
async def get_user_items(user_id:int):
    return read_items_by_uid(user_id)

@router.get("/deleted/{user_id}", response_model=list[ItemModel])
async def get_user_deleted_items(user_id:int):
    # deleted_items: list[ItemModel] = read_deleted_items_by_uid()
    return read_deleted_items_by_uid(user_id)

# @router.get("/{item_id}", response_model=ItemModel)
# async def get_item_by_id(item_id: int):
#     item = read_item_by_id(item_id)
#     if item is None:
#         raise HTTPException(status_code=404, detail={"id": item_id, "message": "Item not found"})
#     return item

@router.post("/", response_model=ItemModel)
def create_new_item_for_user(item: ItemModel):
    return create_item(item)

@router.put("/", response_model=ItemModel)
async def update_item_for_users(item: ItemModel): 
    updated_item: ItemModel = update_item_uid(item.uid, item.id, item.amount)
    if updated_item is None:
        raise HTTPException(
            status_code=404,
            detail={
                "item": item.dict(),  # Convert ItemModel to a dictionary
                "message": "Item not found"
            }
        )
    return updated_item

@router.delete("/{item_id}/{user_id}", response_model=None)
async def delete_existing_item_for_user(item_id: int, user_id:int): 
    # item = read_item_by_id(item_id)
    # if item is None:
    #     raise HTTPException(status_code=404, detail={"id": item_id, "message": "Item not found"})
    delete_item_by_uid(item_id, user_id)