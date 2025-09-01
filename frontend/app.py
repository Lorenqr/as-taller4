# /frontend/app.py

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Mock de productos artesanales (simula datos que vendrían del API Gateway)
items = [
    {"name": "Collar artesanal", "description": "Collar hecho a mano con piedras naturales."},
    {"name": "Bolso de cuero", "description": "Bolso artesanal de cuero genuino con detalles únicos."},
    {"name": "Taza pintada a mano", "description": "Taza de cerámica decorada con pintura artesanal."},
]

@app.route("/")
def index():
    return render_template("index.html", title="ArteSano", items=items)

@app.route("/form", methods=["GET", "POST"])
def new_item():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")

        if name:
            items.append({"name": name, "description": description})

        return redirect(url_for("index"))

    return render_template("form.html", title="Agregar Producto")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
