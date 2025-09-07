FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY ./api-gateway/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./common ./common
COPY ./api-gateway/* ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
