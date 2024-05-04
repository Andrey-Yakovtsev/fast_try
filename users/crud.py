from fastapi import APIRouter
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from users.schemas import CreateUser


async def list_users(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def create_user(session: AsyncSession, user_in: CreateUser) -> CreateUser:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user