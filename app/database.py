from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./app/app.db"

# Adatbázis motor létrehozása
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Fejlesztéshez hasznos, termelésben állítsd False-ra
)

# Session factory létrehozása
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base osztály a modellek számára
Base = declarative_base()

# Dependency injection FastAPI-hoz
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
