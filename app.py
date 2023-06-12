from flask import Flask, jsonify, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import db
import validations as vd
import hashlib
import json
import filetype
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)

file = open('comunas-Chile.json')
comuna_locations = json.load(file)

#Rutas
@app.route("/")
def inicio():
    return render_template("inicio.html")

@app.route("/get-map-data", methods = ['GET'])
@cross_origin(origin='localhost',supports_credentials=True)
def get_map_data():
    if request.method == 'GET':
        comunas_set = set()
        data_donaciones = {}
        for donacion in db.get_five_donacion(0):
            id, comuna, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular = donacion
            comuna, region = db.get_comuna_name_and_region_name_by_comuna_id(comuna)
            if comuna in data_donaciones:
                data_donaciones[comuna].append({
                    'tipo' : tipo,
                    'cantidad' : cantidad,
                    'id' : id,
                    'calle_numero' : calle_numero,
                    'fecha_disponibilidad' : fecha_disponibilidad,
                    'email': email,
                })
            else:
                comunas_set.add(comuna)
                data_donaciones[comuna] = [{
                    'tipo' : tipo,
                    'cantidad' : cantidad,
                    'id' : id,
                    'calle_numero' : calle_numero,
                    'fecha_disponibilidad' : fecha_disponibilidad,
                    'email': email,
                }]
        data_pedidos = {}
        for pedido in db.get_five_pedido(0):
            id, comuna, tipo, descripcion, cantidad, nombre, email, celular = pedido
            comuna, region = db.get_comuna_name_and_region_name_by_comuna_id(comuna)
            if comuna in data_pedidos:
                data_pedidos[comuna].append({
                    'tipo' : tipo,
                    'cantidad' : cantidad,
                    'id' : id,
                    'email': email,
                })
            else:
                comunas_set.add(comuna)
                data_pedidos[comuna] = [{
                    'tipo' : tipo,
                    'cantidad' : cantidad,
                    'id' : id,
                    'email': email,
                }]
        data = {}
        for comuna in comunas_set:
            for comune in comuna_locations:
                if comune["name"] == comuna:
                    print("Comuna:",comuna)
                    data[comune["name"]] = {
                        'lat' : comune["lat"],
                        'lng' : comune["lng"],
                        'donaciones' : data_donaciones.get(comuna),
                        'pedidos' : data_pedidos.get(comuna),
                    }

        return jsonify(data)

@app.route("/get-graphs-data",methods = ['GET'])
@cross_origin(origin='localhost',supports_credentials=True)
def get_graphs_data():
    if request.method == 'GET':
        data = {}
        data['pedidos']=[]
        data['donaciones']=[]
        for dt in db.get_amount_donaciones_by_type():
            data['donaciones'].append([dt[0],dt[1]])
        for dt in db.get_amount_pedidos_by_type():
            data['pedidos'].append([dt[0],dt[1]])
        return jsonify(data)

@app.route("/stats", methods = ['GET'])
def stats():
    if request.method == 'GET':
        return render_template("graficos.html")

@app.route("/donar", methods = ['GET','POST'])
def donar():
    if request.method == 'POST':                                
        c_id, r_id = db.get_comuna_and_region_by_comuna_name(request.form.get('comuna'))
        calle_numero = request.form.get('calle-numero')
        tipo = request.form.get('tipo')
        cantidad = request.form.get('cantidad')
        fecha_disponibilidad = request.form.get('fecha-disponibilidad')
        descripcion = request.form.get('descripcion')
        condiciones = request.form.get('condiciones')
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        celular = request.form.get('celular')
        fotos = []
        fotos.append(request.files.get('foto-1') )
        fotos.append(request.files.get('foto-2') )
        fotos.append(request.files.get('foto-3') )
        if vd.validarDonacion(c_id,r_id,calle_numero,tipo,cantidad,fecha_disponibilidad,nombre,email,celular) and (vd.validate_img(fotos[0]) or vd.validate_img(fotos[1]) or vd.validate_img(fotos[2])):
            id = db.insert_into_donacion(
                                    c_id,
                                    calle_numero,
                                    tipo,
                                    cantidad,
                                    fecha_disponibilidad,
                                    descripcion,
                                    condiciones,
                                    nombre,
                                    email,
                                    celular,
                                )

            for foto in fotos:
                if vd.validate_img(foto):
                    _filename = hashlib.sha256(secure_filename(foto.filename).encode("utf-8")).hexdigest()
                    _extension = filetype.guess(foto).extension
                    img_filename = f"{_filename}.{_extension}"

                    foto.save(os.path.join("static/uploads", img_filename))
                    db.insert_into_foto(img_filename, foto.filename, id)
        return redirect("/")
            
    elif request.method == 'GET':
        return render_template("agregar/agregar-donacion.html")

@app.route("/pedir", methods = ['GET','POST'])
def pedir():
    if request.method == 'POST':
        c_id, r_id = db.get_comuna_and_region_by_comuna_name(request.form.get('comuna'))
        tipo = request.form.get('tipo')
        descripcion = request.form.get('descripcion')
        cantidad = request.form.get('cantidad')
        nombre = request.form.get('nombre')
        mail = request.form.get('email')
        celular = request.form.get('celular')
        msg, status = vd.validarPedido(c_id,r_id,tipo,descripcion,cantidad,nombre,mail,celular)
        if status:
            db.insert_into_pedido(
                                c_id,
                                tipo,
                                descripcion,
                                cantidad,
                                nombre,
                                mail,
                                celular,
                                )
            return redirect("/")
        
        return redirect("/pedir", error = msg)
        
    elif request.method == 'GET':
        return render_template("agregar/agregar-pedido.html")
@app.route("/ver-donaciones/",  defaults={'page': 0}, methods = ['GET'])
@app.route("/ver-donaciones/<int:page>",  methods = ['GET'])
def verDonaciones(page):
    if request.method == 'GET':
        data = []
        rows = db.get_amount_donaciones()[0]
        metadata = {'page':page, 'amount': rows/5}
        for donacion in db.get_five_donacion(page):
            id, comuna, _, tipo, cantidad, fecha_disponibilidad, _, _, nombre, _, _ = donacion
            comuna, region = db.get_comuna_name_and_region_name_by_comuna_id(comuna)
            foto = db.get_foto_by_donacion_id(id)
            _, ruta_archivo, nombre_archivo, donacion_id = foto
            img_filename = "uploads/" + ruta_archivo
            data.append(
                {   
                    'id' : id,
                    'comuna' : comuna,
                    'tipo' : tipo,
                    'cantidad' : cantidad,
                    'fecha_disponibilidad' : fecha_disponibilidad,
                    'nombre' : nombre,
                    'path_image' : url_for('static', filename=img_filename)
                }
            )
        return render_template("ver/ver-donaciones.html", data = data, metadata = metadata)

@app.route("/ver-pedidos/",  defaults={'page': 0}, methods = ['GET'])
@app.route("/ver-pedidos/<int:page>", methods = ['GET'])
def verPedidos(page):
    if request.method == 'GET':
        data = []
        rows = db.get_amount_pedidos()[0]
        metadata = {'page':page, 'amount': rows/5}
        print("----------------------------------------")
        print(metadata)
        print("----------------------------------------")

        for pedido in db.get_five_pedido(page):
            id, comuna, tipo, descripcion, cantidad, nombre, _, _ = pedido
            comuna, region = db.get_comuna_name_and_region_name_by_comuna_id(comuna)
            data.append(
                {   
                    'id' : id,
                    'comuna' : comuna,
                    'tipo' : tipo,
                    'descripcion' : descripcion,
                    'cantidad' : cantidad,
                    'nombre' : nombre,
                }
            )
        return render_template("ver/ver-pedidos.html", data=data, metadata = metadata)

@app.route("/info-donacion/<string:id>", methods = ['GET'])
def infoDonacion(id):
    if request.method == 'GET':
        donacion = db.get_donacion_by_id(id)
        _, comuna, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular = donacion
        fotos = []
        comuna, region = db.get_comuna_name_and_region_name_by_comuna_id(comuna)
        for foto in db.get_fotos_by_donacion_id(id):
            _, ruta_archivo, nombre_archivo, donacion_id = foto
            img_filename = "uploads/" + ruta_archivo
            fotos.append(url_for('static', filename = img_filename))
        data = {        
                            'region' : region,
                            'comuna': comuna,
                            'calle_numero': calle_numero,
                            'tipo': tipo,
                            'cantidad': cantidad,
                            'fecha_disponibilidad': fecha_disponibilidad,
                            'descripcion': descripcion,
                            'condiciones_retirar': condiciones_retirar,
                            'nombre': nombre,
                            'email': email,
                            'celular': celular,
        }
        #PASAR LAS FOTOS TAMBIEN
        return render_template("info/informacion-donacion.html", data=data, fotos=fotos)

@app.route("/info-pedido/<string:id>", methods = ['GET'])
def infoPedido(id):
    if request.method == 'GET':
        pedido = db.get_pedido_by_id(id)
        _, comuna, tipo, descripcion, cantidad, nombre, email, celular = pedido
        comuna, region = db.get_comuna_name_and_region_name_by_comuna_id(comuna)
        
        data = {        
                            'region' : region,
                            'comuna': comuna,
                            'tipo': tipo,
                            'descripcion': descripcion,
                            'cantidad': cantidad,
                            'nombre': nombre,
                            'email': email,
                            'celular': celular,    
        }
        #PASAR LAS FOTOS TAMBIEN
        return render_template("info/informacion-pedido.html", data = data)
