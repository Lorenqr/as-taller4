import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx

# Cargar variables de entorno si existe .env
from dotenv import load_dotenv
load_dotenv()

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")
PRODUCTS_SERVICE_URL = os.getenv("PRODUCTS_SERVICE_URL", "http://products-service:8000")
ORDERS_SERVICE_URL = os.getenv("ORDERS_SERVICE_URL", "http://orders-service:8000")
PAYMENTS_SERVICE_URL = os.getenv("PAYMENTS_SERVICE_URL", "http://payments-service:8000")

app = FastAPI(title="API Gateway")

async def forward_request(request: Request, base_url: str, path: str):
    url = f"{base_url}{path}"
    method = request.method
    headers = dict(request.headers)
    body = await request.body()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method, url, headers=headers, content=body, params=dict(request.query_params)
            )
            return JSONResponse(
                status_code=response.status_code,
                content=response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Error conectando a {base_url}: {str(e)}")

@app.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def auth_proxy(request: Request, path: str):
    return await forward_request(request, AUTH_SERVICE_URL, f"/{path}")

@app.api_route("/products/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def products_proxy(request: Request, path: str):
    return await forward_request(request, PRODUCTS_SERVICE_URL, f"/{path}")

@app.api_route("/orders/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def orders_proxy(request: Request, path: str):
    return await forward_request(request, ORDERS_SERVICE_URL, f"/{path}")

@app.api_route("/payments/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def payments_proxy(request: Request, path: str):
    return await forward_request(request, PAYMENTS_SERVICE_URL, f"/{path}")

@app.get("/")
def root():
    return {"message": "API Gateway funcionando"}

@app.get("/health")
def health():
    return {"status": "ok", "service": "api-gateway"}