import asyncio
from datetime import datetime
import json

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert

from src.roll.models import Roll
from src.config import settings
from src.database import Base, async_session_maker, engine
from src.main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    def open_mock_json(model: str):
        with open(f"src/tests/mock_{model}.json", "r") as file:
            return json.load(file)
    
    roll = open_mock_json("roll")
    
    for item in roll:
        if "date_added" in item:
            item["date_added"] = datetime.strptime(item["date_added"], "%Y-%m-%d").date()
        if "date_removed" in item:
            item["date_removed"] = datetime.strptime(item["date_removed"], "%Y-%m-%d").date()

    
    async with async_session_maker() as session:
        add_cats = insert(Roll).values(roll)
        await session.execute(add_cats)
        await session.commit()
    

@pytest.mark.asyncio(scope="function")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
    

@pytest.fixture(scope="function")
async def ac():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
        
