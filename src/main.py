from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from src.database import test_db_connection

from src.roll.router import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await test_db_connection()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router)