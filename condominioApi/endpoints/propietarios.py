from flask import Blueprint, jsonify, request
from condominioApi.models import Propietario
from condominioApi import db
from condominioApi.schemas import PropietarioSchema
from condominioApi.helpers import existePropietario

from condominioApi.errors import APINotFound, APIBadRequest

# Registrar el endpoint de los propietarios y su schema para la serializacion
propietarios = Blueprint('propietarios', __name__)
propietario_schema = PropietarioSchema()
propietarios_schema = PropietarioSchema(many=True)

@propietarios.get('/')
def get_propietarios():
    # Obtener todos los propietarios de la BBDD
    propietarios = db.session.query(Propietario).all()
    return jsonify(propietarios_schema.dump(propietarios))

@propietarios.get('/<int:propietario_id>/')
def get_propietario(propietario_id):
    # Obtener un propietario por su ID
    propietario = db.session.query(Propietario).filter_by(id=propietario_id).first()
    if not propietario:
        raise APINotFound('Propietario no encontrado')
    return jsonify(propietario_schema.dump(propietario))

@propietarios.post('/')
def add_propietario():
    try:
        # Comprobar que los campos obligatorios sean recibidos
        request.get_json(force=True)
        if not 'nombre' in request.json or not 'apellido' in request.json or not 'email' in request.json:
            raise APIBadRequest('Todos los campos son obligatorios')
        
        # Comprobar que el propietario no sea duplicado
        email = request.json.get('email')
        propietarioExiste = existePropietario(propietarioEmail=email)
        if propietarioExiste:
            raise APIBadRequest('El propietario ya existe')
        
        # Agregar propietario a la base de datos
        propietario = Propietario(
        request.json.get('nombre'),
        request.json.get('apellido'),
        email
        )
        db.session.add(propietario)
    except APIBadRequest:
        raise
    else:
        db.session.commit()
    return jsonify(propietario_schema.dump(propietario))

@propietarios.put('/<int:propietario_id>/')
def update_propietario(propietario_id):
    # Comprobar que el propietario existe para la edicion
    propietario = existePropietario(propietarioId=propietario_id)
    if not propietario:
        raise APINotFound('El propietario no existe')
    try:
        request.get_json(force=True)
        # Comprobar que al editar el email no se este duplicando con otro usuario
        email = request.json.get('email')
        propietarioDuplicado = existePropietario(propietario_id, email)
        if propietarioDuplicado:
            raise APIBadRequest('El correo ya esta en uso')
        
        # Actualizar los campos
        propietario.nombre = request.json.get('nombre', propietario.nombre)
        propietario.apellido = request.json.get('apellido', propietario.apellido)
        propietario.email = request.json.get('email', propietario.email)
    except APIBadRequest:
        raise
    except APINotFound:
        raise
    except:
        raise APIBadRequest('Hubo un error con la peticion')
    else:
        db.session.commit()
    return jsonify(propietario_schema.dump(propietario))

@propietarios.delete('/<int:propietario_id>/')
def delete_propietario(propietario_id):
    # Comprobar que el propietario existe
    propietario = db.session.query(Propietario).filter_by(id=propietario_id).first()
    if not propietario:
        raise APINotFound('El propietario no existe')
    try:
        # Eliminar el propietario de la base de datos
        db.session.delete(propietario)
    except:
        raise APIBadRequest('Hubo un error en la peticion')
    else:
        db.session.commit()
    return jsonify({'msg': 'Propietario eliminado'})