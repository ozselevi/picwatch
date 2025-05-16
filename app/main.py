from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Image, Subscriber
import face_recognition
from PIL import Image as PILImage


Base.metadata.create_all(bind=engine)

# --- Könyvtárak létrehozása ---
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- FastAPI alkalmazás ---
app = FastAPI()

# Statikus fájlok (képek) kezelése
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML sablonok
templates = Jinja2Templates(directory="templates")

# --- Alapértelmezett oldal (index) --- 
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Az adatbázisból lekérjük a képeket
    db = SessionLocal()
    images = db.query(Image).all()
    db.close()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "images": images
    })

# --- Kép feltöltése ---
@app.post("/upload")
async def upload_image(file: UploadFile = File(...), description: str = Form(...)):
    # Kép mentése a fájlrendszerbe
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Face-recognition: arcok számlálása
    image = face_recognition.load_image_file(save_path)
    face_locations = face_recognition.face_locations(image)
    face_count = len(face_locations)

    # Mentés az adatbázisba
    db = SessionLocal()
    new_image = Image(filename=file.filename, description=description, face_count=face_count)
    db.add(new_image)
    db.commit()
    db.close()

    return RedirectResponse(url="/", status_code=303)

# --- Feliratkozás ---
@app.post("/subscribe")
async def subscribe(email: str = Form(...)):
    # Feliratkozás hozzáadása az adatbázishoz
    db = SessionLocal()
    new_subscriber = Subscriber(email=email)
    db.add(new_subscriber)
    db.commit()
    db.close()

    # Visszairányítás a főoldalra
    return RedirectResponse(url="/", status_code=303)
