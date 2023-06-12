import sys
import pymysql

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306
DB_CHARSET = "utf8"

def get_conn():
    conn = pymysql.connect(
        db=DB_NAME,
		user=DB_USERNAME,
		passwd=DB_PASSWORD,
		host=DB_HOST,
		port=DB_PORT,
		charset=DB_CHARSET
    )
    return conn


# DONACIONES
def insert_into_donacion(comuna_id, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular):

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO donacion (comuna_id, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',(comuna_id, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular) )
    conn.commit()
    return cursor.lastrowid

def get_five_donacion(page):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT id, comuna_id, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular FROM donacion ORDER BY id DESC LIMIT %s,5',(page*5,))
    pedidos = cursor.fetchall()
    return pedidos

def get_donacion_by_id(id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT id, comuna_id, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular FROM donacion WHERE id=%s', (id,))
    donacion = cursor.fetchone()
    return donacion

def get_amount_donaciones():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM donacion;')
    amount = cursor.fetchone()
    return amount

def get_amount_donaciones_by_type():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT tipo, COUNT(*) FROM donacion GROUP BY tipo;')
    amount = cursor.fetchall()
    return amount
# PEDIDOS
def insert_into_pedido(comuna_id, tipo, descripcion, cantidad, nombre_solicitante, email_solicitante, celular_solicitante):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO pedido (comuna_id, tipo, descripcion, cantidad, nombre_solicitante, email_solicitante, celular_solicitante) VALUES (%s, %s, %s, %s, %s, %s, %s);',(comuna_id, tipo, descripcion, cantidad, nombre_solicitante, email_solicitante, celular_solicitante) )
    conn.commit()
    return cursor.lastrowid


def get_five_pedido(page):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT id, comuna_id, tipo, descripcion, cantidad, nombre_solicitante, email_solicitante, celular_solicitante FROM pedido ORDER BY id DESC LIMIT %s,5',(page*5,))
    pedidos = cursor.fetchall()
    return pedidos

def get_pedido_by_id(id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT id, comuna_id, tipo, descripcion, cantidad, nombre_solicitante, email_solicitante, celular_solicitante FROM pedido WHERE id=%s',(id,))
    pedido = cursor.fetchone()
    return pedido

def get_amount_pedidos():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM pedido;')
    amount = cursor.fetchone()
    return amount

def get_amount_pedidos_by_type():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT tipo, COUNT(*) FROM pedido GROUP BY tipo;')
    amount = cursor.fetchall()
    return amount

# Comuna
def get_comuna_and_region_by_comuna_name(name):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comuna WHERE nombre=%s',(name,))
    pedido = cursor.fetchone()
    id_comuna, _, region_id = pedido 
    return id_comuna,region_id
def get_comuna_name_and_region_name_by_comuna_id(id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comuna WHERE id=%s',(id,))
    comuna = cursor.fetchone()
    _, nombre_com, region_id = comuna 
    cursor.execute('SELECT * FROM region WHERE id=%s',(region_id,))
    region = cursor.fetchone()
    _, region_name = region
    return nombre_com,region_name

def get_region_name_by_region_id(id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM region WHERE id=%s',(id,))
    region = cursor.fetchone()
    _, region_name = region
    return region_name

# FOTOS

def insert_into_foto(ruta_archivo, nombre_archivo, donacion_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO foto (ruta_archivo, nombre_archivo, donacion_id) VALUES (%s, %s, %s);', (ruta_archivo, nombre_archivo, donacion_id))
    conn.commit()
    return cursor.lastrowid


def get_fotos_by_donacion_id(id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT id, ruta_archivo, nombre_archivo, donacion_id FROM foto WHERE donacion_id=%s',(id,))
    foto = cursor.fetchall()
    return foto

def get_foto_by_donacion_id(id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT id, ruta_archivo, nombre_archivo, donacion_id FROM foto WHERE donacion_id=%s',(id,))
    foto = cursor.fetchone()
    return foto

def get_foto_by_id(id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT id, ruta_archivo, nombre_archivo, donacion_id FROM foto WHERE id=%s',(id,))
    foto = cursor.fetchone()
    return foto