FROM python:3.10

WORKDIR /app

# Rendszerfüggőségek telepítése (dlib-hez is szükségesek!)
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

# CMake frissítése hivatalos binárisról (a pip-es nem mindig működik jól)
RUN wget https://github.com/Kitware/CMake/releases/download/v3.27.9/cmake-3.27.9-linux-x86_64.sh && \
    chmod +x cmake-3.27.9-linux-x86_64.sh && \
    ./cmake-3.27.9-linux-x86_64.sh --skip-license --prefix=/usr/local && \
    rm cmake-3.27.9-linux-x86_64.sh

# Ellenőrizzük, hogy a jó verziót használjuk-e
RUN cmake --version

COPY app/requirements.txt .

# Pip frissítés + függőségek
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/

ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
