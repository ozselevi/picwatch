from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os

app = FastAPI()

# Statikus fájlok (képek)
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML sablonok
templates = Jinja2Templates(directory="templates")

# Feltöltött fájlok tárolása
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Egyszerű memóriabeli tárolók (demo céllal)
uploaded_images = []
subscribed_emails = []

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "images": uploaded_images
    })

@app.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    description: str = Form(...)
):
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    uploaded_images.append({
        "filename": file.filename,
        "description": description
    })

    return RedirectResponse(url="/", status_code=303)

@app.post("/subscribe")
async def subscribe(email: str = Form(...)):
    subscribed_emails.append(email)
    print(f"Új feliratkozó: {email}")
    return RedirectResponse(url="/", status_code=303)
