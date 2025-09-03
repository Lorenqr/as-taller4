from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

# Configuración centralizada
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

async def forward_request(method: str, service_name: str, path: str, request: Request):
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found.")

    url = f"{SERVICES[service_name]}/{path}"
    headers = dict(request.headers)

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            if method in ["POST", "PUT", "PATCH"]:
                body = await request.json()
                resp = await client.request(method, url, headers=headers, json=body, params=request.query_params)
            else:
                resp = await client.request(method, url, headers=headers, params=request.query_params)

        return resp.json()
    except httpx.ConnectError:
        raise HTTPException(status_code=502, detail=f"Service '{service_name}' is unavailable.")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error forwarding request to {service_name}: {e}")

# Rutas genéricas
@router.api_route("/{service_name}/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy(service_name: str, path: str, request: Request):
    return await forward_request(request.method, service_name, path, request)

# Incluir router
app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API Gateway is running."}
