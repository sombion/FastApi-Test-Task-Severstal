from datetime import datetime
import pytest

from src.roll.dao import RollDAO


@pytest.mark.parametrize("min_id,max_id,length,weight,exists", [
    (1, 2, 100, 50, True),
    (2, 3, 150, 60, True),
    (20, 21, 355, 221, False)
])
async def test_filter_roll(min_id, max_id, length, weight, exists):
    filter = {
        "min_id": min_id,
        "max_id": max_id
    }
    roll = await RollDAO.find_by_filter(**filter)
    
    if exists:
        assert roll[0]['length'] == length
        assert roll[0]['weight'] == weight
    else:
        assert not roll


@pytest.mark.parametrize("start_date,end_date,added_count,removed_count,exists", [
    ("2025-03-09", "2025-03-11", 4, 2, True),
    ("2025-05-11", "2025-05-13", 6, 8, False)
])
async def test_stats_roll(start_date, end_date, added_count, removed_count, exists):
    roll = await RollDAO.getting_statistics(
        datetime.strptime(start_date, "%Y-%m-%d").date(), 
        datetime.strptime(end_date, "%Y-%m-%d").date()
    )
    
    if exists:
        assert roll['added_count'] == added_count
        assert roll['removed_count'] == removed_count
    else:
        assert not roll