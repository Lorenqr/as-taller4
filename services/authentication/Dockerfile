FROM python:3.11-slim

WORKDIR /app

# Dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY ./services/authentication/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar uvicorn si no está en requirements.txt
RUN pip install --no-cache-dir uvicorn

COPY ./services/authentication/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Copiar el código del servicio y el código común
COPY ./services/authentication /app
COPY ./common ./common

CMD ["/wait-for-it.sh", "auth-db:27017", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]