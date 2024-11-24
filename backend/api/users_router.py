from fastapi import APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models.UserModels import *
from ..database.items_database import * 

router = APIRouter(
    prefix="/users",  # All routes will have this prefix
    tags=["User"],    # Tag for documentation purposes
)

@router.get("/", response_model=list[UserResponse])
async def get_users():
    return read()

# @router.get("/deleted", response_model=list[UserModel])
# async def get_deleted_users():
#     deleted_users: list[UserModel] = read_deleted()
#     return deleted_users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int):
    user = read_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail={"id": user_id, "message": "user not found"})
    return user

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    return create(user)

# @router.put("/", response_model=None)
# def update_user(user: UserResponse): 
#     updated_user: UserResponse = update(user.id, user.username)
#     if updated_user is None:
#         raise HTTPException(status_code=404, detail={"id": user.id, "message": "user not found"})
#     return updated_user

@router.delete("/{user_id}", response_model=None)
def delete_user(user_id: int): 
    user = read_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail={"id": user_id, "message": "user not found"})
    delete(user_id)