from database import Base, engine
from models import Subscriber, ImageModel

Base.metadata.create_all(bind=engine)
