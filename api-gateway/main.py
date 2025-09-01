from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

# Define la instancia de la aplicación FastAPI.
app = FastAPI(title="API Gateway Taller Microservicios")

# Configura CORS (Cross-Origin Resource Sharing).
# Esto es esencial para permitir que el frontend se comunique con el gateway.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier origen (ajustar en producción)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crea un enrutador para las peticiones de los microservicios.
router = APIRouter(prefix="/api/v1")

# Define los microservicios y sus URLs.
# La URL debe coincidir con el nombre del servicio definido en docker-compose.yml.
# El puerto debe ser el del contenedor (ej. auth-service:8001).
SERVICES = {
    "auth": os.getenv("AUTH_SERVICE_URL", "http://auth-service:8001"),
    "products": os.getenv("PRODUCTS_SERVICE_URL", "http://products-service:8002"),
    "orders": os.getenv("ORDERS_SERVICE_URL", "http://orders-service:8003"),
    "payments": os.getenv("PAYMENTS_SERVICE_URL", "http://payments-service:8004"),
}

# TODO: Implementa una ruta genérica para redirigir peticiones GET.

def get_service_url(service_name: str, path: str) -> str:
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found.")
    return f"{SERVICES[service_name]}/{path}"

# ------------------------------
@router.get("/{service_name}/{path:path}")
async def forward_get(service_name: str, path: str, request: Request):
    service_url = f"{SERVICES[service_name]}/{path}"
    try:
        response = requests.get(service_url, params=request.query_params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error forwarding request to {service_name}: {e}")


@router.post("/{service_name}/{path:path}")
async def forward_post(service_name: str, path: str, request: Request):
    service_url = get_service_url(service_name, path)
    try:
        response = requests.post(service_url, json=await request.json())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error forwarding POST to {service_name}: {e}")


@router.put("/{service_name}/{path:path}")
async def forward_put(service_name: str, path: str, request: Request):
    service_url = get_service_url(service_name, path)
    try:
        response = requests.put(service_url, json=await request.json())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error forwarding PUT to {service_name}: {e}")


@router.delete("/{service_name}/{path:path}")
async def forward_delete(service_name: str, path: str):
    service_url = get_service_url(service_name, path)
    try:
        response = requests.delete(service_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error forwarding DELETE to {service_name}: {e}")

app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API Gateway is running."}