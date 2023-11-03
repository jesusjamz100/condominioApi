from . import db
from sqlalchemy import func
from sqlalchemy.inspection import inspect

class Cuenta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(15), unique=True)
    saldo = db.Column(db.Float)
    ingresos = db.relationship('Ingreso', backref='cuenta')
    egresos = db.relationship('Egreso', backref='cuenta')

    def __init__(self, nombre, saldo):
        self.nombre = nombre
        self.saldo = saldo

class Factura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    egreso_id = db.Column(db.Integer, db.ForeignKey('egreso.id'))
    cantidad = db.Column(db.Float)
    fecha = db.Column(db.DateTime(timezone=True), default=func.now())

    def __init__(self, egreso_id, cantidad):
        self.egreso_id = egreso_id
        self.cantidad = cantidad

class Egreso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cuenta_id = db.Column(db.Integer, db.ForeignKey('cuenta.id'))
    descripcion = db.Column(db.String(30))
    factura = db.relationship('Factura', uselist=False, backref='egreso')

    def __init__(self, cuenta_id, descripcion):
        self.cuenta_id = cuenta_id
        self.descripcion = descripcion

class Recibo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    propietario_id = db.Column(db.Integer, db.ForeignKey('propietario.id'))
    ingreso_id = db.Column(db.Integer, db.ForeignKey('ingreso.id'))
    cantidad = db.Column(db.Float)
    fecha = db.Column(db.DateTime(timezone=True), default=func.now())

    def __init__(self, propietario_id, ingreso_id, cantidad):
        self.propietario_id = propietario_id
        self.ingreso_id = ingreso_id
        self.cantidad = cantidad

class Ingreso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cuenta_id = db.Column(db.Integer, db.ForeignKey('cuenta.id'))
    descripcion = db.Column(db.String(30))
    recibo = db.relationship('Recibo', uselist=False, backref='ingreso')

    def __init__(self, cuenta_id, descripcion):
        self.cuenta_id = cuenta_id
        self.descripcion = descripcion

class Torre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    letra = db.Column(db.String(1), unique=True)
    pisos = db.relationship('Piso', backref='torre')

    def __init__(self, letra):
        self.letra = letra

class Piso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    torre_id = db.Column(db.Integer, db.ForeignKey('torre.id'))
    numero = db.Column(db.Integer)
    apartamentos = db.relationship('Apartamento', backref='piso')
    
    def __init__(self, torre_id, numero):
        self.torre_id = torre_id
        self.numero = numero

class Apartamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    propietario_id = db.Column(db.Integer, db.ForeignKey('propietario.id'))
    piso_id = db.Column(db.Integer, db.ForeignKey('piso.id'))
    codigo = db.Column(db.String(4))

    def __init__(self, propietario_id, piso_id, codigo):
        self.propietario_id = propietario_id
        self.piso_id = piso_id
        self.codigo = codigo
        

class Propietario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30))
    apellido = db.Column(db.String(30))
    email = db.Column(db.String(80), unique=True)
    apartamentos = db.relationship('Apartamento', backref='propietario')
    recibos = db.relationship('Recibo', backref='propietario')

    def __init__(self, nombre, apellido, email):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
