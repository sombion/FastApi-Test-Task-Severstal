from src.roll.dao import RollDAO
from src.exceptions import RollIdNotFound


async def delete_roll(id: int):
    roll = await RollDAO.find_by_id(id)
    if roll is None:
        raise RollIdNotFound
    return await RollDAO.delete(id)

async def filter_roll(
        min_id,
        max_id,
        min_weight,
        max_weight,
        min_length,
        max_length,
        added_from,
        min_date_added,
        min_removed_date,
        max_removed_date
    ):
    filters = {
        "min_id": min_id,
        "max_id": max_id,
        "min_weight": min_weight,
        "max_weight": max_weight,
        "min_length": min_length,
        "max_length": max_length,
        "added_from": added_from,
        "added_to": min_date_added,
        "removed_from": min_removed_date,
        "removed_to": max_removed_date,
    }
    
    filters = {key: value for key, value in filters.items() if value is not None}
    
    return await RollDAO.find_by_filter(**filters)
    

    