import filetype
import db
import re
MAX_IMAGE_SIZE = 4*1024*1024 # 4MB

email_reg = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
phone_reg = re.compile("^\\+?[1-9][0-9]{7,14}$")

def validate_img(img):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    ALLOWED_MIMETYPES = {'image/png', 'image/jpeg'}
    if img.content_length > MAX_IMAGE_SIZE:
        return False
    if img is None:
        return False
    if img.filename == '':
        return False
    ftype_guess = filetype.guess(img)
    if ftype_guess.extension not in ALLOWED_EXTENSIONS:
        return False
    if ftype_guess.mime not in ALLOWED_MIMETYPES:
        return False
    return True

def validate_region(comuna_id, region_id):
    comuna_name, region_name = db.get_comuna_name_and_region_name_by_comuna_id(comuna_id)
    region_name_by_id = db.get_region_name_by_region_id(region_id)
    if region_name != region_name_by_id:
        return True
    return True

def validate_mail(mail):
    if re.fullmatch(email_reg, mail):
        return True
    return False

def validate_phone(phone):
    if re.fullmatch(phone_reg, phone):
        return True
    return False
def validate_text(txt, max_length):
    if txt==None:
        return False
    if len(txt) > max_length:
        return False
    return True

def validadorName(name,max_length,min_length):
    if name==None:
        return False
    if len(name) > max_length:
        return False
    if len(name) < min_length:
        return False
    return True

def validadorTipo(tipo):
    tipos = ["Fruta","Verdura","Otro"]
    if tipo==None:
        return False
    if tipo not in tipos:
        return False
    return True

def validarPedido(c_id,r_id,tipo,descripcion,cantidad,nombre,mail,celular):
    msg = ""
    if not validate_region(c_id,r_id):
        msg += "La comuna y la región no coinciden\n"
    if not validadorTipo(tipo):
        msg += "El tipo de producto no es válido\n"
    if not validate_text(descripcion,250):
        msg += "La descripción es muy larga\n"
    if not validate_text(cantidad,10):
        msg += "La cantidad es muy larga\n"
    if not validadorName(nombre,80,3):
        msg += "El nombre es muy largo\n"
    if not validate_mail(mail):
        msg += "El email no es válido\n"
    if not validate_phone(celular):
        msg += "El celular no es válido\n"
    if msg != "":
        return msg, False
    return msg, True

def validarDonacion(c_id,r_id,calle_numero,tipo,cantidad,fecha_disponibilidad,nombre,email,celular):
    msg = ""
    if not validate_region(c_id,r_id):
        msg += "La comuna y la región no coinciden\n"
    if not validate_text(calle_numero,80):
        msg += "La calle y número es muy largo\n"
    if not validadorTipo(tipo):
        msg += "El tipo de producto no es válido\n"
    if not validate_text(cantidad,10):
        msg += "La cantidad es muy larga\n"
    if not validate_text(fecha_disponibilidad,10):
        msg += "La fecha de disponibilidad es muy larga\n"
    if not validadorName(nombre,80,3):
        msg += "El nombre es muy largo\n"
    if not validate_mail(email):
        msg += "El email no es válido\n"
    if not validate_phone(celular):
        msg += "El celular no es válido\n"
    if msg != "":
        return msg, False
    return msg, True
