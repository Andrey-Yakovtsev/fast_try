import abc
from abc import ABC
from asyncio import current_task
from typing import Sequence, Type

from pydantic.main import Model
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session, AsyncSession

from core.config import settings
from core.models import User, Base


class AbstractRepository(ABC):
    @abc.abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        ...

    @abc.abstractmethod
    def add(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self, *args, **kwargs) -> None:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, url: str, echo: bool = False, echo_pool: bool = False) -> None:
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool
        )
        self.async_session = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False
        )

    async def get(self, model: Model, ref_id: int) -> Model | None:
        async with self.async_session() as session:
            result = await session.get(model, ref_id)
        return result

    async def add(self, obj: Type[Model]) -> None:
        async with self.async_session() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)

    async def list(self, model: Model) -> Sequence[Type[Model]]:
        stmt = select(model).order_by(model.id)
        async with self.async_session() as session:
            result: Result = await session.execute(stmt)
        return result.scalars().all()


repo = SQLAlchemyRepository(url=settings.db_url, echo=settings.echo, echo_pool=settings.echo_pool)