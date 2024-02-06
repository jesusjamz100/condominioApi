from flask import Blueprint, jsonify, request
from condominioApi.models import Egreso
from condominioApi import db
from condominioApi.schemas import EgresoSchema
from condominioApi.helpers import existeEgreso, existeCuenta

from condominioApi.errors import APINotFound, APIBadRequest

# Registrar el endpoint y los schemas de serializacion
egresos = Blueprint('egresos', __name__)
egreso_schema = EgresoSchema()
egresos_schema = EgresoSchema(many=True)

@egresos.get('/')
def get_egresos():
    # Se obtienen todos los egresos de la base de datos
    egresos = db.session.query(Egreso).all()
    return jsonify(egresos_schema.dump(egresos))

@egresos.get('/<int:egreso_id>')
def get_egreso(egreso_id):
    # Obtiene un egreso por su ID
    egreso = existeEgreso(egreso_id)
    if not egreso:
        raise APINotFound('El egreso no existe')
    return jsonify(egreso_schema.dump(egreso))

@egresos.post('/')
def add_egresos():
    try:
        # Comprobar que si viene una data
        data = request.get_json(force=True, silent=True)
        if not data:
            raise APIBadRequest('No se enviaron los datos')
        
        # Comprobar que los datos obligatorios son recibidos
        if not 'cuenta_id' in request.json or not 'descripcion' in request.json:
            raise APIBadRequest('Hubo un error en la peticion')
        
        # Comprobar que la cuenta existe
        cuenta = existeCuenta(int(request.json.get('cuenta_id')))
        if not cuenta:
            raise APINotFound('La cuenta no existe')
        
        # Agregar egreso a la base de datos
        egreso = Egreso(
            cuenta.id,
            request.json.get('descripcion')
        )
        db.session.add(egreso)
    except APIBadRequest:
        raise
    except APINotFound:
        raise
    except:
        raise APIBadRequest('Hubo un error en la peticion')
    else:
        db.session.commit()
    return jsonify(egreso_schema.dump(egreso))

@egresos.put('/<int:egreso_id>')
def update_egreso(egreso_id):
    # Comprobar que el egreso existe
    egreso = existeEgreso(egreso_id)
    if not egreso:
        raise APINotFound('El ingreso no existe')
    
    try:
        # Comprobar si viene unad data
        data = request.get_json(force=True, silent=True)
        if not data:
            raise APIBadRequest('No se enviaron los datos')
        
        # Comprobar que la descripcion no viene vacia
        descripcion = request.json.get('descripcion')
        if descripcion == '':
            raise APIBadRequest('La descripcion es obligatoria')
        
        # Actualizar el egreso
        egreso.descripcion = request.json.get('descripcion', egreso.descripcion)
    except APIBadRequest:
        raise
    except APINotFound:
        raise
    except:
        raise APIBadRequest('Hubo un error en la peticion')
    else:
        db.session.commit()
    return jsonify(egreso_schema.dump(egreso))

@egresos.delete('/<int:egreso_id>')
def delete_egreso(egreso_id):
    # Comprobar que el egreso existe
    egreso = existeEgreso(egreso_id)
    if not egreso:
        raise APINotFound('El egreso no existe')
    try:
        # Eliminar el egreso de la base de datos
        db.session.delete(egreso)
    except:
        raise APIBadRequest('Hubo un error en la peticion')
    else:
        db.session.commit()
    return jsonify({'msg': 'Egreso eliminado'})