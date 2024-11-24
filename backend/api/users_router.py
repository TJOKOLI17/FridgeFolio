from fastapi import APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models.UserModels import *
from ..database.users_database import * 

router = APIRouter(
    prefix="/users",  # All routes will have this prefix
    tags=["User"],    # Tag for documentation purposes
)

@router.get("/", response_model=list[UserResponse])
async def get_users():
    return read_users()

@router.get("/login", response_model=UserResponse)
def get_user_by_password(username:str, password:str):
    user = UserCreate(username=username, password=password)
    sign_in_attempt:UserResponse = read_user_by_password(user)
    if(sign_in_attempt is None):
        raise HTTPException(status_code=404, detail={"username": user.username, "message": "Incorrect username or password"})
    print(sign_in_attempt)
    return sign_in_attempt
        

# @router.get("/deleted", response_model=list[UserModel])
# async def get_deleted_users():
#     deleted_users: list[UserModel] = read_deleted()
#     return deleted_users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int):
    user = read_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail={"id": user_id, "message": "user not found"})
    return user

@router.post("/", response_model=UserResponse)
def create_new_user(user: UserCreate):
    try:
        return create_user(user)
    except ValueError as e:
        if str(e) == "Username already exists":  # Check for specific error message
            raise HTTPException(
                status_code=409,  # Conflict
                detail="A user with this username already exists."
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,  # Internal Server Error
            detail="An unexpected error occurred while creating the user."
        )

# @router.put("/", response_model=None)
# def update_user(user: UserResponse): 
#     updated_user: UserResponse = update(user.id, user.username)
#     if updated_user is None:
#         raise HTTPException(status_code=404, detail={"id": user.id, "message": "user not found"})
#     return updated_user

@router.delete("/{user_id}", response_model=None)
def delete_existing_user(user_id: int): 
    user = read_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail={"id": user_id, "message": "user not found"})
    delete_user(user_id)

# create_new_user(UserCreate(username="testuser", password="testuser123"))
# get_user_by_password(UserCreate(username="testuser", password="testuser123"))
# delete_existing_user(2)