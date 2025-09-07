FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY ./services/orders/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./services/orders/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

COPY ./services/orders ./
COPY ./common ./common

CMD ["/wait-for-it.sh", "orders-db:5432", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
