import httpx
import logging
from typing import Any, Dict, Optional
from datetime import datetime
from common.config import settings
from email_validator import validate_email as ev_validate, EmailNotValidError

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_request_to_service(
    url: str, 
    method: str = "GET", 
    data: Optional[Dict] = None, 
    headers: Optional[Dict] = None
) -> Dict:
    """
    Envía una petición HTTP a otro microservicio de forma asíncrona.

    Args:
        url (str): La URL completa del endpoint.
        method (str): El método HTTP (GET, POST, PUT, DELETE).
        data (Any): Los datos a enviar en el cuerpo de la petición.
        headers (Dict): Headers opcionales.

    Returns:
        dict: La respuesta JSON del servicio.

    Raises:
        httpx.RequestError: Si la petición falla.
    """
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.request(method, url, json=data, headers=headers)
            resp.raise_for_status()
            return resp.json()
    except httpx.RequestError as e:
        logger.error(f"[ERROR] Petición fallida a {url}: {e}")
        raise

def format_date(dt_object: datetime) -> str:
    """Formatea un objeto datetime a una cadena de texto estándar."""
    return dt_object.strftime("%Y-%m-%d %H:%M:%S")

def build_service_url(service: str, endpoint: str) -> str:
    """Construye una URL hacia un microservicio usando settings."""
    base_url = getattr(settings, f"{service.upper()}_SERVICE_URL", None)
    if not base_url:
        raise ValueError(f"El servicio '{service}' no está definido en settings.")
    return f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

def validate_email(email: str) -> bool:
    """Valida un correo electrónico usando email-validator."""
    try:
        ev_validate(email)
        return True
    except EmailNotValidError:
        return False

def current_timestamp() -> str:
    """Devuelve la marca de tiempo actual en formato estandar."""
    return format_date(datetime.utcnow())
