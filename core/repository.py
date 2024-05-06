import abc
from abc import ABC
from asyncio import current_task
from typing import Sequence

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
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False
        )

    def scoped_session(self):
        return async_scoped_session(session_factory=self.session_factory, scopefunc=current_task)

    async def session_dependancy(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependancy(self) -> AsyncSession:
        session = self.scoped_session()
        yield session
        await session.close()

    async def get(self, model: Model, ref_id: int) -> Model | None:
        # FIXME Как валидировать None при обработке несуществующего ключа?
        return await self.scoped_session().get(model, ref_id)

    async def add(self, obj: User) -> None:
        # FIXME Туткак правильно тип подобрать для Обджа?
        self.scoped_session().add(obj)
        await self.scoped_session().commit()

    async def list(self, model: Model) -> Sequence[Model]:
        stmt = select(model).order_by(model.id)
        result: Result = await self.scoped_session().execute(stmt)
        return result.scalars().all()


repo = SQLAlchemyRepository(url=settings.db_url, echo=settings.echo)