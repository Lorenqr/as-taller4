import os
import requests
from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

# Inicializar app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Middleware de sesión (para manejar cookies en frontend)
SECRET_KEY = os.getenv("FRONT_SECRET_KEY", "frontend_secret_key")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# URL del API Gateway (se pasa por docker-compose)
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://localhost:8000")

# =========================
# Rutas principales
# =========================

@app.get("/")
def home(request: Request):
    """Página principal mostrando productos"""
    try:
        resp = requests.get(f"{API_GATEWAY_URL}/products")
        products = resp.json() if resp.status_code == 200 else []
    except Exception:
        products = []
    return templates.TemplateResponse("index.html", {"request": request, "products": products})


# =========================
# Login
# =========================
@app.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(request: Request, response: Response, username: str = Form(...), password: str = Form(...)):
    try:
        resp = requests.post(f"{API_GATEWAY_URL}/auth/login", data={
            "username": username,
            "password": password
        })
        if resp.status_code == 200:
            token = resp.json().get("access_token")
            request.session["token"] = token
            return RedirectResponse(url="/", status_code=303)
        else:
            return templates.TemplateResponse("login.html", {"request": request, "error": "Credenciales inválidas"})
    except Exception:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Error al conectar con el servidor"})


# =========================
# Registro
# =========================
@app.get("/register")
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
def register(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    try:
        resp = requests.post(f"{API_GATEWAY_URL}/auth/register", json={
            "username": username,
            "email": email,
            "password": password
        })
        if resp.status_code == 201:
            return RedirectResponse(url="/login", status_code=303)
        else:
            return templates.TemplateResponse("register.html", {"request": request, "error": "Error en el registro"})
    except Exception:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Error al conectar con el servidor"})


# =========================
# Logout
# =========================
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)
