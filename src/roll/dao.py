from datetime import datetime

from sqlalchemy import delete, func, select
from sqlalchemy.exc import SQLAlchemyError

from src.dao.base import BaseDAO
from src.database import async_session_maker
from src.roll.models import Roll


class RollDAO(BaseDAO):
    model = Roll
    
    @classmethod
    async def find_by_filter(cls, **filters):
        try:
            async with async_session_maker() as session:
                query = select(cls.model.__table__.columns)
                
                if "min_id" in filters:
                    query = query.filter(cls.model.id >= filters["min_id"])
                if "max_id" in filters:
                    query = query.filter(cls.model.id <= filters["max_id"])
                
                if "min_weight" in filters:
                    query = query.filter(cls.model.weight >= filters["min_weight"])
                if "max_weight" in filters:
                    query = query.filter(cls.model.weight <= filters["max_weight"])

                if "min_length" in filters:
                    query = query.filter(cls.model.length >= filters["min_length"])
                if "max_length" in filters:
                    query = query.filter(cls.model.length <= filters["max_length"])

                if "added_from" in filters:
                    query = query.filter(cls.model.date_added >= filters["added_from"])
                if "added_to" in filters:
                    query = query.filter(cls.model.date_added <= filters["added_to"])

                if "removed_from" in filters:
                    query = query.filter(cls.model.date_removed >= filters["removed_from"])
                if "removed_to" in filters:
                    query = query.filter(cls.model.date_removed <= filters["removed_to"])
                    
                result = await session.execute(query)
                return result.mappings().all()
            
        except (SQLAlchemyError, Exception) as e:
            print(f"Ошибка: {e}")
    
    
    @classmethod
    async def delete(cls, id):
        try:
            async with async_session_maker() as session:
                stmt = delete(cls.model).where(cls.model.id==id).returning(cls.model)
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar()
        except (SQLAlchemyError, Exception) as e:
            print(f"Ошибка: {e}")
        
    @classmethod
    async def getting_statistics(cls, start_date: datetime, end_date: datetime):
        try:
            async with async_session_maker() as session:
                added_count = await session.scalar(
                    select(func.count()).where(cls.model.date_added.between(start_date, end_date))
                )

                removed_count = await session.scalar(
                    select(func.count()).where(cls.model.date_removed.between(start_date, end_date))
                )
                
                if added_count == 0 and removed_count == 0:
                    return {}
                
                avg_length = await session.scalar(
                    select(func.avg(cls.model.length)).where(cls.model.date_added <= end_date)
                )
                avg_weight = await session.scalar(
                    select(func.avg(cls.model.weight)).where(cls.model.date_added <= end_date)
                )

                min_length = await session.scalar(
                    select(func.min(cls.model.length)).where(cls.model.date_added <= end_date)
                )
                max_length = await session.scalar(
                    select(func.max(cls.model.length)).where(cls.model.date_added <= end_date)
                )

                min_weight = await session.scalar(
                    select(func.min(cls.model.weight)).where(cls.model.date_added <= end_date)
                )
                max_weight = await session.scalar(
                    select(func.max(cls.model.weight)).where(cls.model.date_added <= end_date)
                )

                total_weight = await session.scalar(
                    select(func.sum(cls.model.weight)).where(cls.model.date_added <= end_date)
                )

                max_storage_time = await session.scalar(
                    select(func.max(cls.model.date_removed - cls.model.date_added))
                    .where(cls.model.date_removed.isnot(None), cls.model.date_added.between(start_date, end_date))
                )
                min_storage_time = await session.scalar(
                    select(func.min(cls.model.date_removed - cls.model.date_added))
                    .where(cls.model.date_removed.isnot(None), cls.model.date_added.between(start_date, end_date))
                )

                min_rolls_day = await session.scalar(
                    select(cls.model.date_added, func.count())
                    .where(cls.model.date_added.between(start_date, end_date))
                    .group_by(cls.model.date_added)
                    .order_by(func.count().asc())
                    .limit(1)
                )

                max_rolls_day = await session.scalar(
                    select(cls.model.date_added, func.count())
                    .where(cls.model.date_added.between(start_date, end_date))
                    .group_by(cls.model.date_added)
                    .order_by(func.count().desc())
                    .limit(1)
                )

                min_weight_day = await session.scalar(
                    select(cls.model.date_added, func.sum(cls.model.weight))
                    .where(cls.model.date_added.between(start_date, end_date))
                    .group_by(cls.model.date_added)
                    .order_by(func.sum(cls.model.weight).asc())
                    .limit(1)
                )

                max_weight_day = await session.scalar(
                    select(cls.model.date_added, func.sum(cls.model.weight))
                    .where(cls.model.date_added.between(start_date, end_date))
                    .group_by(cls.model.date_added)
                    .order_by(func.sum(cls.model.weight).desc())
                    .limit(1)
                )

                return {
                    "added_count": added_count,
                    "removed_count": removed_count,
                    "avg_length": avg_length,
                    "avg_weight": avg_weight,
                    "min_length": min_length,
                    "max_length": max_length,
                    "min_weight": min_weight,
                    "max_weight": max_weight,
                    "total_weight": total_weight,
                    "max_storage_time": max_storage_time,
                    "min_storage_time": min_storage_time,
                    "min_rolls_day": min_rolls_day,
                    "max_rolls_day": max_rolls_day,
                    "min_weight_day": min_weight_day,
                    "max_weight_day": max_weight_day,
                }
        except (SQLAlchemyError, Exception) as e:
            print(f"Ошибка: {e}")