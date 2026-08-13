from contextlib import asynccontextmanager

from fastapi import FastAPI

from football_club_api.db import engine, Base

@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("Application started")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    await engine.dispose()
    print("Application stopped")

app = FastAPI(
    title="Football club API",
    version="1.0.1",
    lifespan=lifespan,
)