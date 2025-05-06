from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import shutil
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Image, Subscriber

# --- Beállítások ---
UPLOAD_DIR = "static/uploads"
DATABASE_PATH = "sqlite:///data/picwatch.db"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)  # Biztosan létezzen az adatbázis mappa

# --- Adatbázis ---
engine = create_engine(DATABASE_PATH, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)  # 🧠 Létrehozza az adatbázist és a táblákat, ha még nem léteznek

# --- FastAPI ---
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- Feltöltött képek listája (memóriában marad a példa kedvéért) ---
uploaded_images = []

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "images": uploaded_images
    })

@app.post("/upload")
async def upload_image(file: UploadFile = File(...), description: str = Form(...)):
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Adatbázisba mentés (opcionális, ha az Image modellt használod)
    db = SessionLocal()
    new_image = Image(filename=file.filename, description=description)
    db.add(new_image)
    db.commit()
    db.close()

    uploaded_images.append({
        "filename": file.filename,
        "description": description
    })

    return RedirectResponse(url="/", status_code=303)

@app.post("/subscribe")
async def subscribe(email: str = Form(...)):
    db = SessionLocal()
    new_subscriber = Subscriber(email=email)
    db.add(new_subscriber)
    db.commit()
    db.close()
    return RedirectResponse(url="/", status_code=303)
