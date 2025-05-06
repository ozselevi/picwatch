from sqlalchemy import Column, Integer, String
from database import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    people_count = Column(Integer, nullable=False, default=0)  # Az emberek számát tároljuk

class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
