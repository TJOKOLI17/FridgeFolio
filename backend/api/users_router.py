from fastapi import APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models.UserModel import UserModel
from ..database.database import * 

router = APIRouter(
    prefix="/users",  # All routes will have this prefix
    tags=["user"],    # Tag for documentation purposes
)

@router.get("/", response_model=list[UserModel])
async def get_users():
    return read()

@router.get("/deleted", response_model=list[UserModel])
async def get_deleted_users():
    deleted_users: list[UserModel] = read_deleted()
    return deleted_users

@router.get("/{user_id}", response_model=UserModel)
async def get_user_by_id(user_id: int):
    user = read_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail={"id": user_id, "message": "user not found"})
    return user

@router.post("/", response_model=UserModel)
def create_user(user: UserModel):
    return create(user)

@router.put("/", response_model=None)
def update_user(user: UserModel): 
    updated_user: UserModel = update(user.id, user.amount)
    if updated_user is None:
        raise HTTPException(status_code=404, detail={"id": user.id, "message": "user not found"})
    return updated_user

@router.delete("/{user_id}", response_model=None)
def delete_user(user_id: int): 
    user = read_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail={"id": user_id, "message": "user not found"})
    delete(user_id)