from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from core.repository import repo
from core.models import Base
from users.views import router as users_router
from adresses.views import router as addrs_router

async def create_db():
    async with repo.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On app startup
    await create_db()
    yield
    # On app shutdown




app = FastAPI(lifespan=lifespan)
app.include_router(users_router)
app.include_router(addrs_router)



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)