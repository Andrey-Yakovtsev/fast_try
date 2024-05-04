

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.bd_helper import db_helper
from users import crud
from users.schemas import CreateUser, UserSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserSchema])
async def list_users(session: AsyncSession = Depends(db_helper.scoped_session_dependancy)):
    return await crud.list_users(session=session)


@router.post("/", response_model=UserSchema)
async def create_users(user: CreateUser, session: AsyncSession = Depends(db_helper.scoped_session_dependancy)):
    user = await crud.create_user(session=session, user_in=user)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.get("/{user_id}/", response_model=UserSchema)
async def get_single_user(user_id: int, session: AsyncSession = Depends(db_helper.scoped_session_dependancy)):
    return await crud.get_user(session=session, user_id=user_id)
