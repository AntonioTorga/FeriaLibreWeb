from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import db
import utils.validations as vd
import hashlib
import filetype
import os
app = Flask(__name__)

#Rutas
@app.route("/")
def inicio():
    return render_template("inicio.html")


@app.route("/donar", methods = ['GET','POST'])
def donar():
    if request.method == 'POST':
        #check validation
                                
        c_id, r_id = db.get_comuna_and_region_by_comuna_name(request.form.get('comuna'))
        #translate comuna to comuna_id
        id = db.insert_into_donacion(
                                c_id,
                                request.form.get('calle-numero'),
                                request.form.get('tipo'),
                                request.form.get('cantidad'),
                                request.form.get('fecha-disponibilidad'),
                                request.form.get('descripcion'),
                                request.form.get('condiciones'),
                                request.form.get('nombre'),
                                request.form.get('email'),
                                request.form.get('celular'),
                             )
        fotos = []
        fotos.append(request.files.get('foto-1') )
        fotos.append(request.files.get('foto-2') )
        fotos.append(request.files.get('foto-3') )

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
    #check validation
        db.insert_into_pedido(c_id,
                                request.form.get('tipo'),
                                request.form.get('descripcion'),
                                request.form.get('cantidad'),
                                request.form.get('nombre'),
                                request.form.get('email'),
                                request.form.get('celular'),
                                )
        return redirect("/")
    elif request.method == 'GET':
        return render_template("agregar/agregar-pedido.html")
@app.route("/ver-donaciones/", defaults= {'page':0})
@app.route("/ver-donaciones/<int:page>",  methods = ['GET'])
def verDonaciones(page):
    if request.method == 'GET':
        data = []
        for donacion in db.get_five_donacion(page):
            id, comuna, _, tipo, cantidad, fecha_disponibilidad, _, _, nombre, _, _ = donacion
            comuna, region = db.get_comuna_name_and_region_name_by_comuna_id(comuna)
            foto = db.get_foto_by_donacion_id(id)
            print(foto)
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
                    #FALTAN LAS FOTOS
                }
            )
        return render_template("ver/ver-donaciones.html", data = data)

@app.route("/ver-pedidos/<int:page>",defaults= {'page':0}, methods = ['GET'])
def verPedidos(page):
    if request.method == 'GET':
        data = []
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
        return render_template("ver/ver-pedidos.html", data=data)

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
