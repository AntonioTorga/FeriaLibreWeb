from flask import Flask, render_template

app = Flask(__name__)

#Rutas
@app.route("/")
def inicio():
    return render_template("inicio.html")

@app.route("/donar")
def donar():
    return render_template("agregar/agregar-donacion.html")

@app.route("/pedir")
def pedir():
    return render_template("agregar/agregar-pedido.html")

@app.route("/ver-donaciones")
def verDonaciones():
    return render_template("ver/ver-donaciones.html")

@app.route("/ver-pedidos")
def verPedidos():
    return render_template("ver/ver-pedidos.html")

@app.route("/info-donacion")
def infoDonacion():
    return render_template("info/informacion-donacion.html")

@app.route("/info-pedido")
def infoPedido():
    return render_template("info/informacion-pedido.html")

