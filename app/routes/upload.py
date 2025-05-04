from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from .. import database, schemas, crud
import os
import shutil

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload-image/")
async def upload_image(
    file: UploadFile = File(...),
    description: str = Form(...),
    db: Session = Depends(database.SessionLocal)
):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image = schemas.ImageCreate(filename=file.filename,
 description=description)
    return crud.create_image(db, image)
