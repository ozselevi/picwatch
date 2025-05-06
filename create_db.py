# create_db.py
import asyncio
from app.database import engine, Base
from app import models  # Fontos, hogy ez betöltődjön!

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_db())
