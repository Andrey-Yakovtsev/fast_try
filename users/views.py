from typing import Type

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.repository import repo
from core.models import User
from users import crud
from users.schemas import CreateUser, UserSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserSchema])
async def list_users():
    return await crud.list_users()


@router.post("/", response_model=UserSchema)
async def create_users(user: CreateUser):
    return await crud.create_user(user_in=user)


@router.get("/{user_id}/", response_model=UserSchema)
async def get_single_user(user_id: int):
    user = await crud.get_user(model=User, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

