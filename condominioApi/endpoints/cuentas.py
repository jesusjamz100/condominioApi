from flask import Blueprint, jsonify, request
from condominioApi.models import Cuenta
from condominioApi import db
from condominioApi.schemas import CuentaSchema

from condominioApi.errors import APINotFound, APIBadRequest

# Registrar el endpoint y el schema de serializacion
cuentas = Blueprint('cuentas', __name__)
cuenta_schema = CuentaSchema()
cuentas_schema = CuentaSchema(many=True)

@cuentas.get('/')
def get_cuentas():
    # Obtener todas las cuentas de la BBDD
    cuentas = db.session.query(Cuenta).all()
    return jsonify(cuentas_schema.dump(cuentas))

@cuentas.get('/<int:cuenta_id>')
def get_cuenta(cuenta_id):
    # Obtener una cuentad por su ID
    cuenta = db.session.query(Cuenta).filter_by(id=cuenta_id).first()
    if not cuenta:
        raise APINotFound('La cuenta no existe')
    return jsonify(cuenta_schema.dump(cuenta))

@cuentas.post('/')
def add_cuenta():
    try:
        request.get_json(force=True)

        # Comprobar que los campos obligatorios sean recibidos
        if not 'nombre' in request.json:
            raise APIBadRequest('El nombre es obligatorio')
        
        # Comprobar que no se crea un duplicado
        cuentaExiste = db.session.query(Cuenta).filter_by(nombre=request.json.get('nombre')).first()
        if cuentaExiste:
            raise APIBadRequest('Esta cuenta ya existe')
        
        # Agregar la cuenta a la base de datos
        cuenta = Cuenta(
            request.json.get('nombre'),
            request.json.get('saldo', 0)
        )
        db.session.add(cuenta)
    except APIBadRequest:
        raise
    except APINotFound:
        raise
    else:
        db.session.commit()
    return jsonify(cuenta_schema.dump(cuenta))

@cuentas.put('/<int:cuenta_id>')
def update_cuenta(cuenta_id):
    # Comprobar que la cuenta existe
    cuenta = db.session.query(Cuenta).filter_by(id=cuenta_id).first()
    if not cuenta:
        APINotFound('La cuenta no existe')
    try:
        request.get_json(force=True)

        # Comprobar que al modificar la cuenta no se este duplicando otra
        nombre = request.json.get('nombre')
        existeCuenta = db.session.query(Cuenta).filter(Cuenta.id != cuenta_id).filter_by(nombre=nombre).first()
        if existeCuenta:
            raise APIBadRequest('La cuenta ya existe')
        
        # Actualizar los campos de la cuenta
        cuenta.nombre = request.json.get('nombre', cuenta.nombre)
        cuenta.saldo = request.json.get('saldo', cuenta.saldo)
    except:
        raise APIBadRequest('Hubo un error en la peticion')
    else:
        db.session.commit()
    return jsonify(cuenta_schema.dump(cuenta))

@cuentas.delete('/<int:cuenta_id>')
def delete_cuenta(cuenta_id):
    # Comprobar que la cuenta existe
    cuenta = db.session.query(Cuenta).filter_by(id=cuenta_id).first()
    if not cuenta:
        APINotFound('La cuenta no existe')
    try:
        # Eliminar la cuenta de la base de datos
        db.session.delete(cuenta)
    except:
        raise APIBadRequest('Hubo un error en la peticion')
    else:
        db.session.commit()
    return jsonify({'msg': 'Cuenta eliminada'})