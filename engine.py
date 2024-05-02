from sqlalchemy.ext.asyncio import create_async_engine


class DbHelper:
    def __init__(self):
        self.engine = create_async_engine("postgresql+asyncpg://fastapi:fastapi@localhost:5432")