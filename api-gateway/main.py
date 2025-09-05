import os
from fastapi import FastAPI, Request, HTTPException
import httpx

# Configuración desde variables de entorno
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")
PRODUCTS_SERVICE_URL = os.getenv("PRODUCTS_SERVICE_URL", "http://products-service:8000")
ORDERS_SERVICE_URL = os.getenv("ORDERS_SERVICE_URL", "http://orders-service:8000")
PAYMENTS_SERVICE_URL = os.getenv("PAYMENTS_SERVICE_URL", "http://payments-service:8000")

app = FastAPI(title="API Gateway", version="1.0.0")


# ---------- UTILIDAD PARA REENVIAR ----------
async def forward_request(method: str, url: str, request: Request):
    try:
        async with httpx.AsyncClient() as client:
            body = await request.body()
            headers = dict(request.headers)

            resp = await client.request(
                method,
                url,
                content=body,
                headers=headers,
                params=request.query_params
            )

            return resp.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Error conectando al servicio: {str(e)}")


# ---------- HEALTH ----------
@app.get("/health")
def health():
    return {"status": "ok", "service": "api-gateway"}


# ---------- AUTH ----------
@app.post("/auth/register")
async def register(request: Request):
    return await forward_request("POST", f"{AUTH_SERVICE_URL}/register", request)

@app.post("/auth/login")
async def login(request: Request):
    return await forward_request("POST", f"{AUTH_SERVICE_URL}/login", request)

@app.get("/auth/me")
async def me(request: Request):
    return await forward_request("GET", f"{AUTH_SERVICE_URL}/users/me", request)


# ---------- PRODUCTS ----------
@app.get("/products")
async def get_products(request: Request):
    return await forward_request("GET", f"{PRODUCTS_SERVICE_URL}/products", request)

@app.post("/products")
async def create_product(request: Request):
    return await forward_request("POST", f"{PRODUCTS_SERVICE_URL}/products", request)


# ---------- ORDERS ----------
@app.get("/orders")
async def get_orders(request: Request):
    return await forward_request("GET", f"{ORDERS_SERVICE_URL}/orders", request)

@app.post("/orders")
async def create_order(request: Request):
    return await forward_request("POST", f"{ORDERS_SERVICE_URL}/orders", request)


# ---------- PAYMENTS ----------
@app.get("/payments")
async def get_payments(request: Request):
    return await forward_request("GET", f"{PAYMENTS_SERVICE_URL}/payments", request)

@app.post("/payments")
async def create_payment(request: Request):
    return await forward_request("POST", f"{PAYMENTS_SERVICE_URL}/payments", request)
