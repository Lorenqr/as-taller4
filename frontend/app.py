# /frontend/app.py

from flask import Flask, render_template, request, redirect, url_for, flash
import os
import requests

app = Flask(__name__)
app.secret_key = "frontend-secret-key"  # Necesaria para flash messages

# URL del API Gateway (definida en docker-compose como variable de entorno)
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")


@app.route("/")
def index():
    """Ruta de la página de inicio: lista de productos"""
    products = []
    try:
        response = requests.get(f"{API_GATEWAY_URL}/api/v1/products/health")
        response.raise_for_status()
        # Aquí deberías apuntar a la ruta real de productos, ej:
        # response = requests.get(f"{API_GATEWAY_URL}/api/v1/products")
        # products = response.json()
        products = [{"name": "Ejemplo Producto", "description": "Descripción de prueba"}]  
    except requests.exceptions.RequestException as e:
        flash(f"Error al conectar con el API Gateway: {e}", "error")

    return render_template("index.html", title="Inicio", products=products)


@app.route("/new-item", methods=["GET", "POST"])
def new_item():
    """Ruta para crear un nuevo producto"""
    if request.method == "POST":
        item_data = {
            "name": request.form.get("name"),
            "description": request.form.get("description"),
        }

        try:
            response = requests.post(
                f"{API_GATEWAY_URL}/api/v1/products", json=item_data
            )
            response.raise_for_status()
            flash("Producto creado exitosamente.", "success")
            return redirect(url_for("index"))
        except requests.exceptions.RequestException as e:
            flash(f"Error al crear el producto: {e}", "error")
            return redirect(url_for("new_item"))

    return render_template("form.html", title="Nuevo Producto")


@app.route("/health")
def health():
    """Ruta para verificar si el frontend está funcionando"""
    return {"status": "ok", "service": "frontend"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
