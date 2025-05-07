# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:your_password@postgres-service:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"host": "postgres-service", "port": "5432"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
