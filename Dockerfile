FROM python:3.10-slim

WORKDIR /app

# Telepítési követelmények
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Teljes app mappa másolása, benne main.py, static/, templates/, stb.
COPY app/ .

# Indítás
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
