from flask import Blueprint, jsonify, request
from condominioApi.models import Ingreso
from condominioApi import db
from condominioApi.schemas import IngresoSchema
from condominioApi.helpers import existeIngreso, existeCuenta

from condominioApi.errors import APINotFound, APIBadRequest

# Registrar el endpoint y los schemas de serializacion
ingresos = Blueprint('ingresos', __name__)
ingreso_schema = IngresoSchema()
ingresos_schema = IngresoSchema(many=True)


@ingresos.get('/')
def get_ingresos():
    # Obtener todos los ingresos de la base de datos
    ingresos = db.session.query(Ingreso).all()
    return jsonify(ingresos_schema.dump(ingresos))

@ingresos.route('/<int:ingreso_id>/', methods=['GET'])
def get_ingreso(ingreso_id):
    # Retorna un ingreso por su ID
    ingreso = db.session.query(Ingreso).filter_by(id=ingreso_id).first()
    if not ingreso:
        raise APINotFound('El ingreso no existe')
    return jsonify(ingreso_schema.dump(ingreso))

@ingresos.post('/')
def add_ingreso():
    try:
        # Comprobar que si viene una data
        data = request.get_json(force=True, silent=True)
        if not data:
            raise APIBadRequest('No se enviaron los datos')
        
        # Comprobar que los datos obligatorios son recibidos
        if not 'cuenta_id' in request.json or not 'descripcion' in request.json:
            raise APIBadRequest('Hubo un error en la peticion')
        
        # Comprobar que la cuenta existe
        cuenta = existeCuenta(data.cuenta_id)
        if not cuenta:
            raise APINotFound('La cuenta no existe')
        
        # Agregar ingreso a la base de datos
        ingreso = Ingreso(
            cuenta.id,
            request.json.get('descripcion')
        )
        db.session.add(ingreso)
    except APIBadRequest:
        raise
    except APINotFound:
        raise
    except:
        raise APIBadRequest('Hubo un error en la peticion')
    else:
        db.session.commit()
    return jsonify(ingreso_schema.dump(ingreso))

@ingresos.put('/<int:ingreso_id>')
def update_ingreso(ingreso_id):
    # Comprobar que el ingreso existe
    ingreso = existeIngreso(ingreso_id)
    if not ingreso:
        raise APINotFound('El ingreso no existe')
    
    try:
        # Comprobar que si viene una data
        data = request.get_json(force=True, silent=True)
        if not data:
            raise APIBadRequest('No se enviaron los datos')
        
        # Comprobar que la descripcion no viene vacia
        descripcion = request.json.get('descripcion')
        if descripcion == '':
            raise APIBadRequest('La descripcion es obligatoria')
        
        # Actualizar el ingreso
        ingreso.descripcion = request.json.get('descripcion', ingreso.descripcion)
    except APIBadRequest:
        raise
    else:
        db.session.commit()
    return jsonify(ingreso_schema.dump(ingreso))

@ingresos.delete('/<int:ingreso_id>')
def delete_ingreso(ingreso_id):
    # Comprobar que el ingreso existe
    ingreso = existeIngreso(ingreso_id)
    if not ingreso:
        raise APINotFound('El ingreso no existe')
    try:
        # Eliminar el ingreso de la base de datos
        db.session.delete(ingreso)
    except:
        raise APIBadRequest('Hubo un error en la peticion')
    else:
        db.session.commit()
    return jsonify({'msg': 'Ingreso eliminado'})