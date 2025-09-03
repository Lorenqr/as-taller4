# /frontend/app.py

from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

# URL del API Gateway (tomado de variable de entorno o fallback local)
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://localhost:8000/api/v1")

# Mock de productos artesanales (si el gateway no responde)
fallback_items = [
    {"name": "Collar artesanal", "description": "Collar hecho a mano con piedras naturales."},
    {"name": "Bolso de cuero", "description": "Bolso artesanal de cuero genuino con detalles únicos."},
    {"name": "Taza pintada a mano", "description": "Taza de cerámica decorada con pintura artesanal."},
]

@app.route("/")
def index():
    try:
        # Llamar al microservicio de productos vía gateway
        response = requests.get(f"{API_GATEWAY_URL}/products/items", timeout=5)
        if response.status_code == 200:
            items = response.json()
        else:
            items = fallback_items
    except requests.exceptions.RequestException:
        items = fallback_items

    return render_template("index.html", title="ArteSano", items=items)

@app.route("/form", methods=["GET", "POST"])
def new_item():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")

        if name:
            try:
                # Enviar al microservicio de productos vía gateway
                requests.post(
                    f"{API_GATEWAY_URL}/products/items",
                    json={"name": name, "description": description},
                    timeout=5
                )
            except requests.exceptions.RequestException:
                # Si falla, lo agregamos al mock local
                fallback_items.append({"name": name, "description": description})

        return redirect(url_for("index"))

    return render_template("form.html", title="Agregar Producto")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
