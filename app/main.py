from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Image, Subscriber
from fastapi import FastAPI
from celery_worker import send_email_notification, send_past_images_to_user
import face_recognition
import cv2
from PIL import Image as PILImage, ImageDraw

Base.metadata.create_all(bind=engine)

# --- Könyvtárak létrehozása ---
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- FastAPI alkalmazás ---
app = FastAPI()

@app.get("/test-celery")
async def test_celery():
    test_task.delay("Hello from FastAPI!")
    return {"message": "Celery task sent!"}

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
    # Kép mentése ideiglenesen
    contents = await file.read()
    original_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(original_path, "wb") as f:
        f.write(contents)

    # Arcok detektálása
    image_np = face_recognition.load_image_file(original_path)
    face_locations = face_recognition.face_locations(image_np)
    people_count = len(face_locations)

    # Arcok bekeretezése
    pil_image = PILImage.fromarray(image_np)
    draw = ImageDraw.Draw(pil_image)
    for top, right, bottom, left in face_locations:
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 255, 0), width=3)

    # Felülírt kép mentése bekeretezve
    pil_image.save(original_path)

    # Adatbázisba mentés
    db = SessionLocal()
    new_image = Image(filename=file.filename, description=description, people_detected=people_count)
    db.add(new_image)
    db.commit()
    db.refresh(new_image)

    # Értesítés
    subscribers = db.query(Subscriber).all()
    for sub in subscribers:
        msg = f"Új kép: {new_image.description}\nArcok száma: {new_image.people_detected}"
        send_email_notification.delay(sub.email, "Új kép érkezett", msg)

    db.close()

    return RedirectResponse(url="/", status_code=303)

# --- Feliratkozás ---
@app.post("/subscribe")
async def subscribe(email: str = Form(...)):
    db = SessionLocal()
    existing = db.query(Subscriber).filter(Subscriber.email == email).first()

    if not existing:
        new_subscriber = Subscriber(email=email)
        db.add(new_subscriber)
        db.commit()

        send_past_images_to_user.delay(email)

    db.close()
    return RedirectResponse(url="/", status_code=303)
