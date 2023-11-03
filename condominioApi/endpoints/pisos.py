from flask import Blueprint, jsonify, request
from condominioApi.models import Piso
from condominioApi import db
from condominioApi.schemas import PisoSchema
from condominioApi.helpers import existeTorre

from condominioApi.errors import APINotFound, APIBadRequest

# Registro del endpoint y schemas para la serializacion
pisos = Blueprint('pisos', __name__)
piso_schema = PisoSchema()
pisos_schema = PisoSchema(many=True)

@pisos.get('/')
def get_pisos():
    # Obtener todos los pisos de la base de datos
    pisos = db.session.query(Piso).all()
    return jsonify(pisos_schema.dump(pisos))

@pisos.get('/<int:piso_id>/')
def get_piso(piso_id):
    # Obtener un piso por su id
    piso = db.session.query(Piso).filter_by(id=piso_id).first()
    if not piso:
        raise APINotFound('El piso no existe')
    return jsonify(piso_schema.dump(piso))

@pisos.post('/')
def add_piso():
    try:
        # Comprobar que se reciben los campos obligatorios
        request.get_json(force=True)
        if not 'torre_id' in request.json or not 'numero' in request.json:
            raise APIBadRequest('Hubo un error en la peticion')
        
        # Comprobar que la torre existe
        torre_id = request.json.get('torre_id')
        if not existeTorre(torre_id):
            raise APINotFound('La torre no existe')
        
        # Comprobar que no es duplicado
        numero = request.json.get('numero')
        existePiso = db.session.query(Piso).filter_by(torre_id=torre_id).filter_by(numero=numero).first()
        if existePiso:
            raise APIBadRequest('El piso ya existe')
        
        # Crear el piso en la base de datos
        piso = Piso(torre_id, numero)
        db.session.add(piso)
    except APIBadRequest:
        raise
    else:
        db.session.commit()
    return jsonify(piso_schema.dump(piso))

@pisos.put('/<int:piso_id>/')
def update_piso(piso_id):
    piso = db.session.query(Piso).filter_by(id=piso_id).first()
    if not piso:
        raise APINotFound('El piso no existe')
    try:
        request.get_json(force=True)

        # Evitar que al actualizar el piso sea un duplicado
        numeroPiso = request.json.get('numero')
        pisoExiste = db.session.query(Piso).filter(Piso.id!=piso_id).filter_by(numero=numeroPiso).filter_by(torre_id=piso.torre_id).first()
        if pisoExiste:
            raise APIBadRequest('No se puede modificar el numero de piso porque ya existe')
        
        # Actualizar el piso
        piso.numero = request.json.get('numero', piso.numero)
    except APIBadRequest:
        raise
    else:
        db.session.commit()
    return jsonify(piso_schema.dump(piso))

@pisos.delete('/<int:piso_id>/')
def delete_piso(piso_id):
    # Comprobar que el piso existe
    piso = db.session.query(Piso).filter_by(id=piso_id).first()
    if not piso:
        raise APINotFound('El piso no existe')
    try:
        # Eliminar el piso
        db.session.delete(piso)
    except:
        raise APINotFound('Hubo un erro en la peticion')
    else:
        db.session.commit()
    return jsonify({'msg': 'El piso ha sido eliminado'})