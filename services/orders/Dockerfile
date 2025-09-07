FROM python:3.11-slim

WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY ./services/orders/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

COPY ./services/orders ./app
COPY ./common ./common

CMD ["/wait-for-it.sh", "orders-db:27017", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
