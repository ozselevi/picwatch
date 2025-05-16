from sqlalchemy import Column, Integer, String
from database import Base

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    description = Column(String)
    face_count = Column(Integer, default=0)

class Subscriber(Base):
    __tablename__ = "subscribers"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
