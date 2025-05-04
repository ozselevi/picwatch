from fastapi import FastAPI
from . import models, database
from .routes import upload

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(upload.router)
