# /frontend/app.py

from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# URL del API Gateway
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://localhost:8000/api/v1")


fallback_items = [
    {"name": "Collar artesanal", "description": "Collar hecho a mano con piedras naturales."},
    {"name": "Bolso de cuero", "description": "Bolso artesanal de cuero genuino con detalles únicos."},
    {"name": "Taza pintada a mano", "description": "Taza de cerámica decorada con pintura artesanal."},
]


# Rutas principales

@app.route("/")
def index():
    try:
        response = requests.get(f"{API_GATEWAY_URL}/products/items", timeout=5)
        items = response.json() if response.status_code == 200 else fallback_items
    except requests.exceptions.RequestException:
        items = fallback_items
    return render_template("index.html", title="ArteSano", items=items)


@app.route("/form", methods=["GET", "POST"])
def new_item():
    # Requiere login
    if "token" not in session:
        flash("Debes iniciar sesión primero 🔒", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")

        if name:
            try:
            
                headers = {"Authorization": f"Bearer {session['token']}"}
                requests.post(
                    f"{API_GATEWAY_URL}/products/items",
                    json={"name": name, "description": description},
                    headers=headers,
                    timeout=5
                )
            except requests.exceptions.RequestException:
                fallback_items.append({"name": name, "description": description})

        return redirect(url_for("index"))

    return render_template("form.html", title="Agregar Producto")


# Autenticación
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            response = requests.post(
                f"{API_GATEWAY_URL}/auth/login",
                data={"username": email, "password": password},
                timeout=5
            )

            if response.status_code == 200:
                token = response.json().get("access_token")
                session["token"] = token
                flash("Inicio de sesión exitoso ✅", "success")
                return redirect(url_for("index"))
            else:
                flash("Credenciales inválidas ❌", "danger")

        except requests.exceptions.RequestException:
            flash("Error al conectar con el servidor de autenticación ⚠️", "danger")

    return render_template("login.html", title="Iniciar Sesión")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role", "user")

        try:
            response = requests.post(
                f"{API_GATEWAY_URL}/auth/register",
                json={"email": email, "password": password, "role": role},
                timeout=5
            )
            if response.status_code == 201:
                flash("Registro exitoso 🎉, ahora inicia sesión", "success")
                return redirect(url_for("login"))
            else:
                flash("Error al registrarse ❌", "danger")
        except requests.exceptions.RequestException:
            flash("Servicio de autenticación no disponible ⚠️", "danger")

    return render_template("register.html", title="Registrarse")


@app.route("/logout")
def logout():
    session.pop("token", None)
    flash("Sesión cerrada 👋", "info")
    return redirect(url_for("index"))


# Main
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
