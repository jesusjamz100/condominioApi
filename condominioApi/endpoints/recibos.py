from flask import Blueprint, jsonify, request
from condominioApi import db
from condominioApi.helpers import (
    agregarIngreso, 
    existeIngreso, 
    existePropietario, 
    ingresoTieneRecibo, 
    existeRecibo, 
    actualizarSaldo
)
from condominioApi.models import Recibo
from condominioApi.schemas import ReciboSchema

from condominioApi.errors import APIBadRequest, APINotFound

# Regsitrar el endpoint y los schemas de serializacion
recibos = Blueprint('recibos', __name__)
recibo_schema = ReciboSchema()
recibos_schema = ReciboSchema(many=True)

@recibos.get('/')
def get_recibos():
    # Obtener todos los recibos
    recibos = db.session.query(Recibo).all()
    return jsonify(recibos_schema.dump(recibos))

@recibos.get('/<int:recibo_id>')
def get_recibo(recibo_id):
    # Obtener un recibo por su ID
    recibo = existeRecibo(recibo_id)
    if not recibo:
        APINotFound('El recibo no existe')
    return jsonify(recibo_schema.dump(recibo))

@recibos.post('/')
def add_recibo():
    try:
        # Comprobar que si viene una data
        data = request.get_json(force=True, silent=True)
        if not data:
            raise APIBadRequest('No se enviaron los datos')
        
        # Comprobar que los datos obligatorios son recibidos
        if not 'propietario_id' in request.json or not 'ingreso_id' in request.json or not 'cantidad' in request.json:
            raise APIBadRequest('Todos los datos son obligatorios')
        
        # Comprobar que el ingreso y el propietario existen
        ingreso = existeIngreso(request.json.get('ingreso_id'))
        if not ingreso:
            raise APINotFound('El ingreso no existe')
        propietario = existePropietario(request.json.get('propietario_id'))
        if not propietario:
            raise APINotFound('El propietario no existe')
        
        # Comprobar que el ingreso no tenga ya un recibo
        if ingresoTieneRecibo(ingreso):
            raise APIBadRequest('El ingreso ya tiene un recibo')
        
        # Agregar el recibo a la base de datos
        cantidad = request.json.get('cantidad')
        recibo = Recibo(propietario.id, ingreso.id, cantidad)
        db.session.add(recibo)

        # Actualizar el saldo de la cuenta
        agregarIngreso(ingreso.cuenta_id, cantidad)

    except APIBadRequest:
        raise
    except APINotFound:
        raise
    except:
        raise APIBadRequest('Hubo un error con la peticion')
    else:
        db.session.commit()
    return jsonify(recibo_schema.dump(recibo))

@recibos.put('/<int:recibo_id>')
def update_recibo(recibo_id):
    # Comprobar que el recibo existe
    recibo = existeRecibo(recibo_id)
    if not recibo:
        raise APINotFound('El recibo no existe')
    try:
        # Comprobar que si viene data
        data = request.get_json(force=True, silent=True)
        if not data:
            raise APIBadRequest('No se enviaron los datos')
        
        # Extraer datos del request
        cantidad = request.json.get('cantidad')
        fecha = request.json.get('fecha')

        # Comprobar que los datos obligatorios no estan vacios
        if cantidad == '' or fecha == '':
            raise APIBadRequest('La cantidad y la fecha son obligatorios')
        
        # Actualizar el saldo de la cuenta
        actualizarSaldo(cantidad, recibo=recibo)

        # Actualizar el recibo
        recibo.cantidad = cantidad if cantidad else recibo.cantidad
        recibo.fecha = fecha if fecha else recibo.fecha
        
    except APIBadRequest:
        raise
    except APINotFound:
        raise
    else:
        db.session.commit()
    return jsonify(recibo_schema.dump(recibo))

@recibos.delete('/<int:recibo_id>')
def delete_recibo(recibo_id):
    # Comprobar que el recibo existe
    recibo = existeRecibo(recibo_id)
    if not recibo:
        raise APINotFound('El recibo no existe')
    try:
        # Actualizar el saldo de la cuenta
        actualizarSaldo(0, recibo=recibo)

        # Eliminar el recibo de la base de datos
        db.session.delete(recibo)
    except APINotFound:
        raise
    except:
        raise APIBadRequest('Hubo un error en la peticion')
    else:
        db.session.commit()
    return jsonify({'msg': 'Recibo eliminado'})