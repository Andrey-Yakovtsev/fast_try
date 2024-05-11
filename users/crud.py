from core.repository import repo
from core.models import User
from users.schemas import CreateUser


async def list_users() -> list[User]:
    users = await repo.list(model=User)
    return list(users)


async def get_user(model: User, user_id: int) -> User | None:
    return await repo.get(model=model, ref_id=user_id)


async def create_user(user_in: CreateUser) -> User:
    user = User(**user_in.model_dump())
    await repo.add(obj=user)
    return user
