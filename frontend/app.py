import os
import requests
from fastapi import FastAPI, Request, Form, Response, UploadFile, File
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
    if not request.session.get("email"):
        return RedirectResponse("/login")
    return templates.TemplateResponse("index.html", {"request": request, "session": request.session})

@app.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "session": request.session})

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
            # Obtener datos del usuario (incluyendo el rol)
            userinfo = requests.get(
                f"{API_GATEWAY_URL}/auth/me",
                headers={"Authorization": f"Bearer {token}"},
                timeout=5
            )
            if userinfo.status_code == 200:
                user_data = userinfo.json()
                request.session["token"] = token
                request.session["email"] = email
                request.session["role"] = user_data.get("role")
                return RedirectResponse("/", status_code=303)
            else:
                return templates.TemplateResponse(
                    "login.html",
                    {"request": request, "session": request.session, "error": "No se pudo obtener información del usuario"},
                    status_code=401
                )
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
def register_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    role: str = Form(...)
):
    try:
        response = requests.post(
            f"{API_GATEWAY_URL}/auth/register",
            json={"email": email, "password": password, "full_name": full_name, "role": role},
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

@app.get("/add-product", response_class=HTMLResponse)
def add_product_get(request: Request):
    if request.session.get("role") != "vendedor":
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("add_product.html", {"request": request})

@app.post("/add-product", response_class=HTMLResponse)
def add_product_post(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    image: UploadFile = File(None)
):
    if request.session.get("role") != "vendedor":
        return RedirectResponse("/", status_code=303)
    image_url = None
    if image:
        uploads_dir = os.path.join("static", "uploads")
        os.makedirs(uploads_dir, exist_ok=True)
        file_location = os.path.join(uploads_dir, image.filename)
        with open(file_location, "wb") as buffer:
            buffer.write(image.file.read())
        image_url = f"/static/uploads/{image.filename}"
    try:
        response = requests.post(
            f"{API_GATEWAY_URL}/products/",
            json={
                "name": name,
                "description": description,
                "price": price,
                "stock": stock,
                "image": image_url
            },
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