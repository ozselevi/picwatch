FROM python:3.10-slim

# Munkakönyvtár beállítása
WORKDIR /app

# Szükséges fájlok és wheels mappa másolása
COPY app/requirements.txt .
COPY wheels/ /tmp/wheels/

# Csomagok telepítése (face-recognition és függőségei csak a wheels-ből)
RUN pip install --no-cache-dir --no-index --find-links=/tmp/wheels face-recognition \
 && pip install --no-cache-dir -r requirements.txt

# Teljes app könyvtár másolása
COPY app/ /app/

# PYTHONPATH beállítása, hogy a /app mappát tartalmazza
ENV PYTHONPATH=/app

# Alkalmazás indítása (FastAPI)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
