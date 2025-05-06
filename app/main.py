from fastapi import FastAPI, Request, Form, UploadFile, File, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os

from app import crud, models, schemas
from app.database import get_db

from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

# Statikus fájlok
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: AsyncSession = Depends(get_db)):
    images = await crud.get_images(db)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "images": images
    })


@app.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    description: str = Form(...),
    people_count: int = Form(...),
    db: AsyncSession = Depends(get_db)
):
    # Kép mentése a fájlrendszerbe
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Kép metaadatainak mentése az adatbázisba
    image_in = schemas.ImageCreate(
        filename=file.filename,
        description=description,
        people_count=people_count
    )
    await crud.create_image(db, image=image_in)

    return RedirectResponse(url="/", status_code=303)


@app.post("/subscribe")
async def subscribe(email: str = Form(...), db: AsyncSession = Depends(get_db)):
    subscriber = schemas.SubscriberCreate(email=email)
    await crud.create_subscriber(db, subscriber=subscriber)
    print(f"Új feliratkozó: {email}")
    return RedirectResponse(url="/", status_code=303)
