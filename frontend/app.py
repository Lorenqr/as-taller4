import os
import requests
from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")
FRONT_SECRET_KEY = os.getenv("FRONT_SECRET_KEY", "frontend_secret_key")

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=FRONT_SECRET_KEY)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "session": request.session})

@app.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "session": request.session})

@app.get("/cart", response_class=HTMLResponse)
def cart(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request})

@app.post("/login")
def login_post(request: Request, email: str = Form(...), password: str = Form(...)):
    try:
        response = requests.post(
            f"{API_GATEWAY_URL}/auth/login",
            data={"username": email, "password": password},
            timeout=5
        )
        if response.status_code == 200:
            token = response.json()["access_token"]
            request.session["token"] = token
            request.session["email"] = email
            return RedirectResponse("/", status_code=303)
        else:
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "session": request.session, "error": "Credenciales incorrectas"},
                status_code=401
            )
    except Exception:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "session": request.session, "error": "Error de conexión con el API Gateway"},
            status_code=502
        )

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)

@app.get("/register", response_class=HTMLResponse)
def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "session": request.session})

@app.post("/register")
def register_post(request: Request, email: str = Form(...), password: str = Form(...), full_name: str = Form(None)):
    try:
        response = requests.post(
            f"{API_GATEWAY_URL}/auth/register",
            json={"email": email, "password": password, "full_name": full_name},
            timeout=5
        )
        if response.status_code == 200:
            return RedirectResponse("/login", status_code=303)
        else:
            return templates.TemplateResponse(
                "register.html",
                {"request": request, "session": request.session, "error": response.json().get("detail", "Error en el registro")},
                status_code=400
            )
    except Exception:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "session": request.session, "error": "Error de conexión con el API Gateway"},
            status_code=502
        )

@app.get("/products", response_class=HTMLResponse)
def products(request: Request):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        response = requests.get(f"{API_GATEWAY_URL}/products/", headers=headers, timeout=5)
        if response.status_code == 200:
            products = response.json()
            return templates.TemplateResponse("products.html", {"request": request, "session": request.session, "products": products})
        else:
            return templates.TemplateResponse(
                "products.html",
                {"request": request, "session": request.session, "error": "No se pudieron obtener los productos"},
                status_code=502
            )
    except Exception:
        return templates.TemplateResponse(
            "products.html",
            {"request": request, "session": request.session, "error": "Error de conexión con el API Gateway"},
            status_code=502
        )

# --- NUEVO: Agregar producto ---
@app.get("/add-product", response_class=HTMLResponse)
def add_product_get(request: Request):
    return templates.TemplateResponse("add_product.html", {"request": request})

@app.post("/add-product", response_class=HTMLResponse)
def add_product_post(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...)
):
    try:
        response = requests.post(
            f"{API_GATEWAY_URL}/products/",
            json={"name": name, "description": description, "price": price, "stock": stock},
            timeout=5
        )
        if response.status_code == 200:
            return templates.TemplateResponse(
                "add_product.html",
                {"request": request, "success": "Producto agregado correctamente"}
            )
        else:
            return templates.TemplateResponse(
                "add_product.html",
                {"request": request, "error": "Error al agregar el producto"}
            )
    except Exception:
        return templates.TemplateResponse(
            "add_product.html",
            {"request": request, "error": "No se pudo conectar con el API Gateway"}
        )
