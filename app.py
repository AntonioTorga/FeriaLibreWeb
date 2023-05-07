from flask import Flask, render_template

app = Flask(__name__)

#Rutas
@app.route("/")
def inicio():
    return render_template("inicio.html")

# @app.route("/donar")

# @app.route("/pedir")

# @app.route("/ver-donaciones")

# @app.route("/ver-pedidos")

# @app.route("/info-donacion")

# @app.route("/info-pedido")