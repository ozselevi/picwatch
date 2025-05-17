FROM python:3.10

WORKDIR /app

# Rendszercsomagok a buildhez és dlib-hez
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    wget \
    unzip \
    git \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libboost-python-dev \
    && rm -rf /var/lib/apt/lists/*

# CMake frissítése (a pip-es nem mindig jó dlib-hez)
RUN wget https://github.com/Kitware/CMake/releases/download/v3.27.9/cmake-3.27.9-linux-x86_64.sh && \
    chmod +x cmake-3.27.9-linux-x86_64.sh && \
    ./cmake-3.27.9-linux-x86_64.sh --skip-license --prefix=/usr/local && \
    rm cmake-3.27.9-linux-x86_64.sh

# Ellenőrzés: jó verzió legyen!
RUN cmake --version

# dlib forráskód letöltése + pybind11 frissítése benne
RUN git clone https://github.com/davisking/dlib.git /dlib && \
    cd /dlib && \
    git checkout v19.24 && \
    rm -rf dlib/external/pybind11 && \
    git clone https://github.com/pybind/pybind11.git dlib/external/pybind11

# requirements.txt átmásolása (face_recognition csak ez után!)
COPY app/requirements.txt .

# pip frissítése
RUN pip install --upgrade pip

# dlib forrásból fordítása
RUN pip install /dlib

# További csomagok telepítése (face_recognition, uvicorn, stb.)
RUN pip install --no-cache-dir -r requirements.txt

# App fájlok átmásolása
COPY app/ /app/

ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
