FROM python:3.10-slim

# Rendszer szintű csomagok telepítése a face_recognition-hoz
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libssl-dev \
    libffi-dev \
    libopencv-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Munkakönyvtár beállítása
WORKDIR /app

# Szükséges fájlok másolása
COPY app/requirements.txt .

# Python csomagok telepítése
RUN pip install --no-cache-dir -r requirements.txt

# Teljes app könyvtár másolása
COPY app/ /app/

# PYTHONPATH beállítása
ENV PYTHONPATH=/app

# FastAPI indítása
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
