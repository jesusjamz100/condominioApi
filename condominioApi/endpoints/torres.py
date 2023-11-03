from flask import Blueprint, jsonify, request
from condominioApi.models import Torre
from condominioApi import db
from condominioApi.schemas import TorreSchema

from condominioApi.errors import APINotFound, APIBadRequest

# Registra el endpoint de las torres y el schema de serializacion
torres = Blueprint('torres', __name__)
torre_schema = TorreSchema()
torres_schema = TorreSchema(many=True)

@torres.get('/')
def get_torres():
    # Obtener todas las torres de la BBDD
    torres = db.session.query(Torre).all()
    return jsonify(torres_schema.dump(torres))

@torres.get('/<int:torre_id>/')
def get_torre(torre_id):
    # Obtener una torre en especifico por su ID
    torre = db.session.query(Torre).filter_by(id=torre_id).first()

    # Comprobar que existe la torre
    if not torre:
        raise APINotFound('Torre no encontrada')
    return jsonify(torre_schema.dump(torre))

@torres.post('/')
def add_torre():
    try:
        request.get_json(force=True)
        # Comprobar el campo obligatorio para la creacion de la Torre
        if not 'letra' in request.json:
            raise APIBadRequest('Todos los campos son obligatorios')
        
        # Comprobar que la torre no existe para evitar duplicados
        existeTorre = db.session.query(Torre).filter_by(letra=request.json.get('letra')).first()
        if existeTorre:
            raise APIBadRequest('La torre ya existe')
        
        # Agregar la torre a la base de datos
        torre = Torre(request.json.get('letra'))
        db.session.add(torre)
    except APIBadRequest:
        raise
    else:
        db.session.commit()
    return jsonify(torre_schema.dump(torre))

@torres.put('/<int:torre_id>/')
def update_torre(torre_id):
    # Comprobar que la torre existe
    torre = db.session.query(Torre).filter_by(id=torre_id).first()
    if not torre:
        raise APINotFound('La torre no existe')
    try:
        # Comprobar que al editar la torre no se duplique otra torre
        request.get_json(force=True)
        torreExiste = db.session.query(Torre).filter(Torre.id != torre_id).filter_by(letra=request.json.get('letra')).first()
        if torreExiste:
            raise APIBadRequest('La torre ya existe')
        
        # Editar la informacion
        torre.letra = request.json.get('letra', torre.letra)
    except APIBadRequest:
        raise
    else:
        db.session.commit()
    return jsonify(torre_schema.dump(torre))

@torres.delete('/<int:torre_id>/')
def delete_torre(torre_id):
    # Comprobar que existe la torre
    torre = db.session.query(Torre).filter_by(id=torre_id).first()
    if not torre:
        raise APINotFound('La torre no existe')
    try:
        # Eliminar la torre
        db.session.delete(torre)
    except:
        raise APIBadRequest('Hubo un error en la peticion')
    else:
        db.session.commit()
    return jsonify({'msg': 'La torre ha sio eliminada'})