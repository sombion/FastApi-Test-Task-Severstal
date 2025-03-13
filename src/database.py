import asyncpg
from sqlalchemy import NullPool
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.config import settings


async def test_db_connection():
    try:
        engine = create_async_engine(settings.DATABASE_URL)
        async with engine.begin() as conn:
            await conn.run_sync(lambda connection: print("БД успешно подключена"))
        await engine.dispose()
        return True
    except asyncpg.exceptions.InvalidPasswordError:
        print("Ошибка: Неверный пароль для подключения к PostgreSQL.")
    except OperationalError as e:
        print(f"Ошибка подключения к базе данных: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass