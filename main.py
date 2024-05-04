from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from core.bd_helper import db_helper
from core.models import Base
from users.views import router as users_router

async def create_db():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On app startup
    await create_db()
    yield
    # On app shutdown




app = FastAPI(lifespan=lifespan)
app.include_router(users_router)



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)