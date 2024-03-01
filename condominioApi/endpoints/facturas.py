from flask import Blueprint, jsonify, request
from condominioApi import db
from condominioApi.helpers import (
    agregarEgreso, 
    existeEgreso,
    egresoTieneFactura, 
    existeFactura, 
    actualizarSaldo
)
from condominioApi.models import Factura
from condominioApi.schemas import FacturaSchema

from condominioApi.errors import APIBadRequest, APINotFound

# Registrar el endpoint y los schemas de serializacion
facturas = Blueprint('facturas', __name__)
factura_schema = FacturaSchema()
facturas_schema = FacturaSchema(many=True)

@facturas.get('/')
def get_facturas():
    # Obtener todos las facturas
    facturas = db.session.query(Factura).all()
    return jsonify(facturas_schema.dump(facturas))

@facturas.get('/<int:factura_id>')
def get_factura(factura_id):
    # Obtener una factura por su ID
    factura = existeFactura(factura_id)
    if not factura:
        raise APINotFound('La factura no existe')
    return jsonify(factura_schema.dump(factura))

@facturas.post('/')
def add_factura():
    try:
        # Comprobar que si viene data
        data = request.get_json(force=True, silent=True)
        if not data:
            raise APIBadRequest('No se enviaron los datos')
        
        # Comprobar que los datos obligatorios son recibidos
        if not 'egreso_id' in request.json or not 'cantidad' in request.json:
            raise APIBadRequest('Todos los campos son obligatorios')
        
        # Comprobar que el egreso existe
        egreso = existeEgreso(request.json.get('egreso_id'))
        if not egreso:
            raise APINotFound('El egreso no existe')
        
        # Comprobar que el egreso no tenga ya una factura
        if egresoTieneFactura(egreso):
            raise APIBadRequest('El egreso ya tiene una factura')
        
        # Agregar la factura a la base de datos
        cantidad = request.json.get('cantidad')
        factura = Factura(egreso.id, cantidad)
        db.session.add(factura)

        # Actualizar el saldo de la cuenta
        agregarEgreso(egreso.cuenta_id, float(cantidad))

    except APIBadRequest:
        raise
    except APINotFound:
        raise
    else:
        db.session.commit()
    return jsonify(factura_schema.dump(factura))

@facturas.put('/<int:factura_id>')
def update_factura(factura_id):
    # Comprobar que el recibo existe
    factura = existeFactura(factura_id)
    if not factura:
        raise APINotFound('La factura no existe')
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
        actualizarSaldo(float(cantidad), factura=factura)

        # Actualizar el recibo
        factura.cantidad = cantidad if cantidad else factura.cantidad
        # factura.fecha = fecha if fecha else factura.fecha
        
    except APIBadRequest:
        raise
    except APINotFound:
        raise
    else:
        db.session.commit()
    return jsonify(factura_schema.dump(factura))

@facturas.delete('/<int:factura_id>')
def delete_factura(factura_id):
    # Comprobar que el factura existe
    factura = existeFactura(factura_id)
    if not factura:
        raise APINotFound('La factura no existe')
    try:
        # Actualizar el saldo de la cuenta
        actualizarSaldo(0, factura=factura)

        # Eliminar la factura de la base de datos
        db.session.delete(factura)
    except APINotFound:
        raise
    except:
        raise APIBadRequest('Hubo un error en la peticion')
    else:
        db.session.commit()
    return jsonify({'msg': 'Factura eliminada'})