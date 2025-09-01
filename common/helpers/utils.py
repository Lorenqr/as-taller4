import json
import requests
from typing import Any, Dict, Optional
from datetime import datetime
from common.config import settings

def send_request_to_service(url: str, method: str = "GET", data: Optional[Dict] = None) -> Dict:
    """
    Envía una petición HTTP a otro microservicio.
    
    Args:
        url (str): La URL completa del endpoint.
        method (str): El método HTTP (GET, POST, PUT, DELETE).
        data (Any): Los datos a enviar en el cuerpo de la petición (para POST/PUT).
    
    Returns:
        dict: La respuesta del servicio en formato JSON.
    
    Raises:
        requests.exceptions.RequestException: Si la petición falla.
    """
    try:
        response = requests.request(method, url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Peticion fallida s {url}: {e}")
        raise


def format_date(dt_object: datetime) -> str:
    """Formatea un objeto datetime a una cadena de texto."""
    return dt_object.strftime("%Y-%m-%d %H:%M:%S")


def build_service_url(service: str, endpoint: str) -> str:
# ------------------------------------------------------------------------------
# Ejemplo de uso en un microservicio
# from common.helpers.utils import send_request_to_service
# from common.config import settings
# 
# URL del servicio de autenticación
# auth_url = f"{settings.AUTH_SERVICE_URL}/users"
# 
# try:
#     # Envía una petición para obtener todos los usuarios del servicio de autenticación
#     users = send_request_to_service(auth_url)
#     print("Usuarios obtenidos:", users)
# except requests.exceptions.RequestException:
#     print("No se pudo obtener la lista de usuarios.")
#
    base_url = getattr(settings, f"{service.upper()}_SERVICE_URL", None)
    if not base_url:
            raise ValueError(f"El servicio '{service}' no está definido en settings.")
    return f"{base_url}{endpoint}"

def validate_email(email: str) -> bool:
    """Valida si una cadena es un correo electrónico válido."""
    import re
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def current_timestamp() -> str:
    """Devuelve la marca de tiempo actual en formato estandar"""
    return format_date(datetime.utcnow())