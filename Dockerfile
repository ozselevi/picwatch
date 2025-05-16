# Használj egy hivatalos Python 3.10-es alap image-et
FROM python:3.10-slim

# Frissítés és alap build függőségek telepítése (dlib, face_recognition miatt)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libboost-all-dev \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libatlas-base-dev \
    python3-dev \
    libdlib-dev \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*

# Munkakönyvtár beállítása
WORKDIR /app

# Másold be a requirements.txt-t és telepítsd a Python függőségeket
COPY app/requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Másold be a teljes kódot
COPY /app /app

# Alap parancs a futtatáshoz (pl. FastAPI)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
