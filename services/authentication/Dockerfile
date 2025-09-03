# Imagen base de Python
FROM python:3.11-slim

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la app
COPY . .

# Exponer el puerto del servicio de autenticación
EXPOSE 8001

# Comando para correr FastAPI con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
