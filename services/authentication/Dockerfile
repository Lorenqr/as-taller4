FROM python:3.11-slim

WORKDIR /app


# Dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias
COPY ./services/authentication/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del servicio y el código común
COPY ./services/authentication /app
COPY ./common ./common


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
