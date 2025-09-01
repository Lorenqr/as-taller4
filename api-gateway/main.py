from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

# Importar configuración centralizada
from common.config import settings


# Inicialización de la app
app = FastAPI(title="API Gateway Taller Microservicios")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api/v1")


# Definición de microservicios
SERVICES = {
    "auth": settings.AUTH_SERVICE_URL,
    "products": settings.PRODUCTS_SERVICE_URL,
    "orders": settings.ORDERS_SERVICE_URL,
    "payments": settings.PAYMENTS_SERVICE_URL,
}


# Rutas genéricas para proxy
@router.get("/{service_name}/{path:path}")
async def forward_get(service_name: str, path: str, request: Request):
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found.")
    try:
        response = requests.get(f"{SERVICES[service_name]}/{path}", params=request.query_params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error forwarding request to {service_name}: {e}")

@router.post("/{service_name}/{path:path}")
async def forward_post(service_name: str, path: str, request: Request):
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found.")
    try:
        response = requests.post(f"{SERVICES[service_name]}/{path}", json=await request.json())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error forwarding request to {service_name}: {e}")

@router.put("/{service_name}/{path:path}")
async def forward_put(service_name: str, path: str, request: Request):
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found.")
    try:
        response = requests.put(f"{SERVICES[service_name]}/{path}", json=await request.json())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error forwarding request to {service_name}: {e}")

@router.delete("/{service_name}/{path:path}")
async def forward_delete(service_name: str, path: str):
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found.")
    try:
        response = requests.delete(f"{SERVICES[service_name]}/{path}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error forwarding request to {service_name}: {e}")


# Incluir router
app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API Gateway is running."}
