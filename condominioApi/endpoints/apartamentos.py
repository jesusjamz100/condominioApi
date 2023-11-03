from flask import Blueprint, request, jsonify
from condominioApi.models import Apartamento
from condominioApi import db
from condominioApi.schemas import ApartamentoSchema
from condominioApi.helpers import existePiso, existePropietario

from condominioApi.errors import APINotFound, APIBadRequest

# Registrar el endpoint y los schemas para la serializacion
apartamentos = Blueprint('apartamentos', __name__)
apartamento_schema = ApartamentoSchema()
apartamentos_schema = ApartamentoSchema(many=True)

@apartamentos.get('/')
def get_apartamentos():
    # Obtener todos los apartamentos de la base de datos
    apartamentos = db.session.query(Apartamento).all()
    return jsonify(apartamentos_schema.dump(apartamentos))

@apartamentos.get('/<int:apartamento_id>')
def get_apartamento(apartamento_id):
    # Obtener un apartamento por ID
    apartamento = db.session.query(Apartamento).filter_by(id=apartamento_id).first()
    if not apartamento:
        raise APINotFound('El apartamento no existe')
    return jsonify(apartamento_schema.dump())

@apartamentos.post('/')
def add_apartamento():
    try:
        request.get_json(force=True)

        # Comprobar que los datos obligatorios son recibidos
        if not 'codigo' in request.json or not 'propietario_id' in request.json or not 'piso_id' in request.json:
            raise APIBadRequest('Hubo un error en la peticion')
        
        # Comprobar que el piso y el propietario existen
        piso_id = request.json.get('piso_id')
        propietario_id = request.json.get('propietario_id')
        if not existePiso(piso_id):
            raise APINotFound('El piso no existe')
        if not existePropietario(propietario_id):
            raise APINotFound('El propietario no existe')
        
        # Comprobar que no sea duplicado
        codigo = request.json.get('codigo')
        existeApartamento = db.session.query(Apartamento).filter_by(piso_id=piso_id).filter_by(codigo=codigo).first()
        if existeApartamento:
            raise APIBadRequest('El apartamento ya existe')
        
        # Agregar apartamento a la base de datos
        apartamento = Apartamento(propietario_id, piso_id, codigo)
        db.session.add(apartamento)
    except APINotFound:
        raise
    except APIBadRequest:
        raise
    else:
        db.session.commit()
    return jsonify(apartamento_schema.dump(apartamento))

@apartamentos.put('/<int:apartamento_id>')
def update_apartamento(apartamento_id):
    # Comprobar que el apartamento existe
    apartamento = db.session.query(Apartamento).filter_by(id=apartamento_id).first()
    if not apartamento:
        raise APINotFound('El apartamento no existe')
    try:
        request.get_json(force=True)

        # Comprobar que al actualizar el apartamento no se este duplicando otro
        apartamentoCodigo = request.json.get('codigo')
        apartamentoExiste = db.session.query(Apartamento).filter(Apartamento.id != apartamento_id).filter_by(codigo=apartamentoCodigo).filter_by(piso_id=apartamento.piso_id).first()
        if apartamentoExiste:
            raise APIBadRequest('El apartamento ya existe')
        
        # Actualizar el apartamento
        apartamento.codigo = request.json.get('codigo', apartamento.codigo)
    except APIBadRequest:
        raise
    else:
        db.session.commit()
    return jsonify(apartamento_schema.dump(apartamento))

@apartamentos.delete('/<int:apartamento_id>')
def delete_apartamento(apartamento_id):
    # Comprobar que el apartamento existe
    apartamento = db.session.query(Apartamento).filter_by(id=apartamento_id).first()
    if not apartamento:
        APINotFound('El apartamento no existe')
    try:
        # Eliminar el apartamento
        db.session.delete(apartamento)
    except:
        APIBadRequest('Hubo un problema con la peticion')
    else:
        db.session.commit()
    return jsonify({'msg': 'El apartamento ha sido eliminado'})