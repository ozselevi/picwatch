FROM python:3.10-slim

# Munkakönyvtár beállítása
WORKDIR /app

# Szükséges fájlok másolása
COPY app/requirements.txt .

# Csomagok telepítése
RUN pip install --no-cache-dir -r requirements.txt

# Teljes app könyvtár másolása
COPY app/ /app/

# PYTHONPATH beállítása, hogy a /app mappát tartalmazza
ENV PYTHONPATH=/app

# Alkalmazás indítása (FastAPI)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
