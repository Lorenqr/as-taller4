from fastapi import FastAPI, Request, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
import os

API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")

app = FastAPI(title="Frontend - E-commerce Artesanal")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Simulación de sesión en memoria
session = {"token": None, "email": None, "role": None, "cart": []}


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "session": session})


# ========== AUTENTICACIÓN ==========
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                f"{API_GATEWAY_URL}/auth/login",
                data={"username": email, "password": password}
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError:
            return RedirectResponse("/login?error=1", status_code=status.HTTP_302_FOUND)

        data = resp.json()
        session["token"] = data["access_token"]
        session["email"] = email

    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
async def register(email: str = Form(...), password: str = Form(...), role: str = Form("cliente")):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                f"{API_GATEWAY_URL}/auth/register",
                json={"email": email, "password": password, "role": role}
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError:
            return RedirectResponse("/register?error=1", status_code=status.HTTP_302_FOUND)

    return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)


@app.get("/logout")
def logout():
    session.clear()
    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)


# ========== PRODUCTOS ==========
@app.get("/products", response_class=HTMLResponse)
async def products(request: Request):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_GATEWAY_URL}/products")
        products = resp.json()

    return templates.TemplateResponse("products.html", {"request": request, "products": products, "session": session})


@app.post("/add-to-cart")
async def add_to_cart(product_id: str = Form(...), name: str = Form(...), price: float = Form(...)):
    session["cart"].append({"id": product_id, "name": name, "price": price})
    return RedirectResponse("/cart", status_code=status.HTTP_302_FOUND)


# ========== CARRITO ==========
@app.get("/cart", response_class=HTMLResponse)
def view_cart(request: Request):
    total = sum(item["price"] for item in session["cart"])
    return templates.TemplateResponse("cart.html", {"request": request, "cart": session["cart"], "total": total, "session": session})


# ========== CHECKOUT / PEDIDOS ==========
@app.get("/checkout", response_class=HTMLResponse)
def checkout_page(request: Request):
    total = sum(item["price"] for item in session["cart"])
    return templates.TemplateResponse("checkout.html", {"request": request, "cart": session["cart"], "total": total, "session": session})


@app.post("/checkout")
async def checkout():
    if not session.get("token"):
        return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)

    order_data = {
        "user": session["email"],
        "items": session["cart"],
        "total": sum(item["price"] for item in session["cart"])
    }

    async with httpx.AsyncClient() as client:
        # Crear pedido
        await client.post(f"{API_GATEWAY_URL}/orders", json=order_data)

        # Procesar pago
        await client.post(f"{API_GATEWAY_URL}/payments", json={
            "user": session["email"],
            "amount": order_data["total"]
        })

    session["cart"].clear()
    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
