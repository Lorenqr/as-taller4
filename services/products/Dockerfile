FROM python:3.11-slim

WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY ./services/products/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./services/products/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

COPY ./services/products ./
COPY ./common ./common

CMD ["/wait-for-it.sh", "products-db:5432", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
