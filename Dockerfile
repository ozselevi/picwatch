FROM python:3.10-slim

# Beállítjuk a munkakönyvtárat
WORKDIR /app

# Először a requirements.txt fájlt másoljuk és telepítjük a szükséges csomagokat
COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Másoljuk az app mappát (benne a static, templates és egyéb fájlokkal) a konténerbe
COPY app /app
COPY app/static /app/static

# A parancs, ami elindítja az alkalmazást
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
