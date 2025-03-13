from datetime import datetime
import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("length,weight,date_added,date_removed,status_code", [
    (200, 300, "2025-03-10", "2025-03-13", 200),
    (-1, 400, "2025-03-09", "2025-03-13", 422),
    (400, 500, "2025-03-02", "2025-03-13", 200)
])
async def test_add_roll(length, weight, date_added, date_removed, status_code, ac: AsyncClient):
    response = await ac.post("/roll/add", json={
        "length": length,
        "weight": weight,
        "date_added": datetime.strptime(date_added, "%Y-%m-%d").date().isoformat(),
        "date_removed": datetime.strptime(date_removed, "%Y-%m-%d").date().isoformat(),
    })
    
    assert response.status_code == status_code

@pytest.mark.parametrize("id,status_code", [
    (6, 200),
    (20, 404),
])
async def test_del_roll(id, status_code, ac: AsyncClient):
    response = await ac.delete(f"/roll/delete/{id}")
    assert response.status_code == status_code