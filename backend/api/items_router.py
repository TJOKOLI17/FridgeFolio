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
    return read()

@router.get("/deleted", response_model=list[ItemModel])
async def get_deleted_items():
    deleted_items: list[ItemModel] = read_deleted()
    return deleted_items

@router.get("/{item_id}", response_model=ItemModel)
async def get_item_by_id(item_id: int):
    item = read_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail={"id": item_id, "message": "Item not found"})
    return item

@router.post("/", response_model=ItemModel)
def create_item(item: ItemModel):
    return create(item)

@router.put("/", response_model=None)
def update_item(item: ItemModel): 
    updated_item: ItemModel = update(item.id, item.amount)
    if updated_item is None:
        raise HTTPException(status_code=404, detail={"id": item.id, "message": "Item not found"})
    return updated_item

@router.delete("/{item_id}", response_model=None)
def delete_item(item_id: int): 
    item = read_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail={"id": item_id, "message": "Item not found"})
    delete(item_id)

"""
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from .models.ItemModel import ItemModel
# from ..database.database import * 

# app = FastAPI(root_path="/items")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust the origin as necessary
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
#     allow_headers=["*"],  # Allows all headers
# )

# @app.get("/", response_model=list[ItemModel], tags=["Item"])
# async def get_items():
#     return read()

# #thrown away page
# @app.get("/deleted", response_model=list[ItemModel], tags=["Item"])
# async def get_deleted_items():
#     deleted_items:list[ItemModel] = read_deleted()
#     # if deleted_items is None:
#     #     raise HTTPException(status_code=404, detail={"message": "Items not found"})
#     return deleted_items

# @app.get("/{item_id}", response_model=ItemModel, tags=["Item"])
# async def get_item_by_id(item_id:int):
#     item = read_by_id(item_id)
#     if item is None:
#         raise HTTPException(status_code=404, detail={"id": item_id, "message": "Item not found"})
#     return read_by_id(item_id)

# @app.post("/", response_model=ItemModel, tags=["Item"])
# def create_item(item: ItemModel):
#     return create(item)
    
# @app.put("/", response_model=None, tags=["Item"])
# def update_item(item: ItemModel): 
#     updated_item:ItemModel = update(item.id, item.amount)
#     if updated_item is None:
#         raise HTTPException(status_code=404, detail={"id": item.id, "message": "Item not found"})
#     return updated_item

# @app.delete("/{item_id}", response_model=None, tags=["Item"])
# def delete_item(item_id:int): 
#     item = read_by_id(item_id)
#     if item is None:
#         raise HTTPException(status_code=404, detail={"id": item_id, "message": "Item not found"})
#     delete(item_id)
"""