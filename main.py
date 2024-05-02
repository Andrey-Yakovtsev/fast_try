from contextlib import asynccontextmanager

from fastapi import FastAPI

async def create_db():
    ...


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On app startup
    await create_db()
    yield
    # On app shutdown



app = FastAPI(lifespan=lifespan)



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
