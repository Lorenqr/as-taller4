import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Clase para gestionar las configuraciones globales del proyecto."""


    # Configuración General
    PROJECT_NAME: str = "Ecommerce Microservices"
    VERSION: str = "0.1.0"


    # API Gateway
    API_GATEWAY_URL: str = os.getenv("API_GATEWAY_URL", "http://localhost:8000")


    # Microservicios (urls internas en Docker)
    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8001")
    PRODUCTS_SERVICE_URL: str = os.getenv("PRODUCTS_SERVICE_URL", "http://products-service:8002")
    ORDERS_SERVICE_URL: str = os.getenv("ORDERS_SERVICE_URL", "http://orders-service:8003")
    PAYMENTS_SERVICE_URL: str = os.getenv("PAYMENTS_SERVICE_URL", "http://payments-service:8004")


    # Bases de datos
    AUTH_DB_URL: str = os.getenv("AUTH_DB_URL", "mongodb://auth-db:27017/")
    PRODUCTS_DB_URL: str = os.getenv("PRODUCTS_DB_URL", "postgresql://postgres:postgres@products-db:5432/products_db")
    ORDERS_DB_URL: str = os.getenv("ORDERS_DB_URL", "postgresql://postgres:postgres@orders-db:5432/orders_db")
    PAYMENTS_DB_URL: str = os.getenv("PAYMENTS_DB_URL", "postgresql://postgres:postgres@payments-db:5432/payments_db")


    # JWT (autenticación y seguridad)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# Instancia global de configuraciones
settings = Settings()
