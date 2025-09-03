from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuraciones globales del proyecto."""

    # Configuración General
    PROJECT_NAME: str = "Ecommerce Microservices"
    VERSION: str = "0.1.0"

    # API Gateway
    API_GATEWAY_URL: str = "http://localhost:8000"

    # Microservicios (urls internas en Docker)
    AUTH_SERVICE_URL: str = "http://authentication:8001"
    PRODUCTS_SERVICE_URL: str = "http://products:8002"
    ORDERS_SERVICE_URL: str = "http://orders:8003"
    PAYMENTS_SERVICE_URL: str = "http://payments:8004"

    # Bases de datos
    AUTH_DB_URL: str = "mongodb://auth-mongo:27017/"
    PRODUCTS_DB_URL: str = "postgresql://postgres:postgres@products-db:5432/products_db"
    ORDERS_DB_URL: str = "postgresql://postgres:postgres@orders-db:5432/orders_db"
    PAYMENTS_DB_URL: str = "postgresql://postgres:postgres@payments-db:5432/payments_db"

    # JWT (autenticación y seguridad)
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instancia global de configuraciones
settings = Settings()

