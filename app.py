from flask import Flask, render_template, request
import db
app = Flask(__name__)

#Rutas
@app.route("/")
def inicio():
    return render_template("inicio.html")

@app.route("/donar", methods = ['GET','POST'])
def donar():
    if request.method == 'POST':
        #check validation
        db.insert_into_donacion(
                                request.form.get('comuna'),
                                request.form.get('calle-numero'),
                                request.form.get('tipo'),
                                request.form.get('cantidad'),
                                request.form.get('fecha_disponibilidad'),
                                request.form.get('descripcion'),
                                request.form.get('condiciones_retirar'),
                                request.form.get('nombre'),
                                request.form.get('email'),
                                request.form.get('celular'),
                             )
    elif request.method == 'GET':
        return render_template("agregar/agregar-donacion.html")

@app.route("/pedir", methods = ['GET','POST'])
def pedir():
    if request.method == 'POST':
    #check validation
        db.insert_into_pedido(request.form.get('comuna'),
                                request.form.get('tipo'),
                                request.form.get('descripcion'),
                                request.form.get('cantidad'),
                                request.form.get('nombre'),
                                request.form.get('email'),
                                request.form.get('celular'),
                                )
    elif request.method == 'GET':
        return render_template("agregar/agregar-pedido.html")

@app.route("/ver-donaciones/<int:page>", defaults= {'page':0},  methods = ['GET'])
def verDonaciones(page):
    if request.method == 'GET':
        data = []
        for donacion in db.get_five_donacion(page):
            _, comuna, _, tipo, cantidad, fecha_disponibilidad, _, _, nombre, _, _ = donacion
            data.append({
                {
                    'comuna' : comuna,
                    'tipo' : tipo,
                    'cantidad' : cantidad,
                    'fecha-disponibilidad' : fecha_disponibilidad,
                    'nombre' : nombre,
                    #FALTAN LAS FOTOS
                }
            })
        return render_template("ver/ver-donaciones.html", data = data)

@app.route("/ver-pedidos/<int:page>",defaults= {'page':0}, methods = ['GET'])
def verPedidos(page):
    if request.method == 'GET':
        data = []
        for pedido in db.get_five_pedido(page):
            _, comuna, tipo, descripcion, cantidad, nombre, _, _ = pedido
            data.append({
                {
                    'comuna' : comuna,
                    'tipo' : tipo,
                    'descripcion' : descripcion,
                    'cantidad' : cantidad,
                    'nombre' : nombre,
                }
            })
        return render_template("ver/ver-pedidos.html", data=data)

@app.route("/info-donacion/<string:id>", methods = ['GET'])
def infoDonacion(id):
    if request.method == 'GET':
        data = []
        for donacion in db.get_donacion_by_id(id):
            region = 0 # HAY Q OBTENER REGION CON ID COMUNA
            _, comuna, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular = donacion
            data.append({        
                                'region' : region,
                                'comuna': comuna,
                                'calle-numero': calle_numero,
                                'tipo': tipo,
                                'cantidad': cantidad,
                                'fecha_disponibilidad': fecha_disponibilidad,
                                'descripcion': descripcion,
                                'condiciones_retirar': condiciones_retirar,
                                'nombre': nombre,
                                'email': email,
                                'celular': celular,
                                
            })
        #PASAR LAS FOTOS TAMBIEN
        return render_template("info/informacion-donacion.html", data=data)

@app.route("/info-pedido", methods = ['GET'])
def infoPedido():
    if request.method == 'GET':
        data = []
        for pedido in db.get_donacion_by_id(id):
            region = 0 # HAY Q OBTENER REGION CON ID COMUNA
            _, comuna, tipo, descripcion, cantidad, nombre, email, celular = pedido
            data.append({        
                                'region' : region,
                                'comuna': comuna,
                                'tipo': tipo,
                                'descripcion': descripcion,
                                'cantidad': cantidad,
                                'nombre': nombre,
                                'email': email,
                                'celular': celular,    
            })
        #PASAR LAS FOTOS TAMBIEN
        return render_template("info/informacion-pedido.html", data = data)
