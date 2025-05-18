FROM python:3.10-slim

WORKDIR /app

COPY app/requirements.txt .
COPY wheels/ /tmp/wheels/

RUN pip install --no-cache-dir --no-index --find-links=/tmp/wheels face-recognition \
 && pip install --no-cache-dir -r requirements.txt

COPY app/ /app/

ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
