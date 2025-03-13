from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError

from src.database import async_session_maker


class BaseDAO:
    model = None
    
    @classmethod
    async def find_by_id(cls, model_id: int):
        try:
            async with async_session_maker() as session:
                query = select(cls.model).filter_by(id=model_id)
                result = await session.execute(query)
                return result.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            print(f"Ошибка: {e}")
        
    @classmethod
    async def find_all(cls, **filter_by):
        try:
            async with async_session_maker() as session:
                query = select(cls.model.__table__.columns).filter_by(**filter_by)
                result = await session.execute(query)
                return result.mappings().all()
        except (SQLAlchemyError, Exception) as e:
            print(f"Ошибка: {e}")
        
    @classmethod
    async def add(cls, **data):
        try:
            async with async_session_maker() as session:
                stmt = insert(cls.model).values(data).returning(cls.model)
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar()
        except (SQLAlchemyError, Exception) as e:
            print(f"Ошибка: {e}")