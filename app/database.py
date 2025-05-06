# database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --- Könyvtárak létrehozása, ha nem léteznek ---
os.makedirs("data", exist_ok=True)

# --- Adatbázis elérési út ---
DATABASE_URL = "sqlite:///data/picwatch.db"

# --- SQLAlchemy engine ---
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# --- Session létrehozása ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Base osztály, amelyből minden modell származik ---
Base = declarative_base()
