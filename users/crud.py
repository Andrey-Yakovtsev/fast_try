from fastapi import APIRouter
from pydantic.main import Model
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.repository import repo
from core.models import User
from users.schemas import CreateUser, UserSchema, BaseUserModel


async def list_users() -> list[User]:
    users = await repo.list(model=User)
    return list(users)


async def get_user(model: User, user_id: int) -> User | None:
    return await repo.get(model=model, ref_id=user_id)


async def create_user(user_in: UserSchema) -> BaseUserModel:
    print("creating user", user_in)
    user = User(**user_in.model_dump())
    print("user==>", user)
    # FIXME Надо создавать без ID... Что-то со схемой намутил...
    await repo.add(obj=user)
    return user
