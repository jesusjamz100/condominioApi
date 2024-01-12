from condominioApi import db
from condominioApi.models import *

# Verificar la existencia de tablas padre para la creacion de hijos

def existePiso(pisoId: int) -> Piso:
    piso = db.session.query(Piso).filter_by(id=pisoId).first()
    return piso

def existePropietario(propietarioId: int=None, propietarioEmail: str=None) -> Propietario:
    ''' Al declarar el ID y el Email busca un propietario por el email que tenga un ID diferente para comprobaciones de uso de email al actualizar '''
    if propietarioId and not propietarioEmail:
        # Buscar por ID
        propietario = db.session.query(Propietario).filter_by(id=propietarioId).first()
    elif propietarioEmail and not propietarioId:
        # Buscar a cualquiera con el email
        propietario = db.session.query(Propietario).filter_by(email=propietarioEmail).first()
    elif propietarioId and propietarioEmail:
        # Buscar por email que sea diferente ID
        propietario = db.session.query(Propietario).filter(Propietario.id != propietarioId).filter_by(email=propietarioEmail).first()
    return propietario

def existeTorre(torreId: int) -> Torre:
    torre = db.session.query(Torre).filter_by(id=torreId).first()
    return torre

def existeIngreso(ingresoId: int) -> Ingreso:
    ingreso = db.session.query(Ingreso).filter_by(id=ingresoId).first()
    return ingreso

def existeCuenta(cuentaId: int) -> Cuenta:
    cuenta = db.session.query(Cuenta).filter_by(id=cuentaId).first()
    return cuenta

def ingresoTieneRecibo(ingreso: Ingreso):
    return ingreso.__getattribute__('recibo')

def egresoTieneFactura(egreso: Egreso):
    return egreso.__getattribute__('factura')

def existeRecibo(reciboId: int) -> Recibo:
    recibo = db.session.query(Recibo).filter_by(id=reciboId).first()
    return recibo

def existeEgreso(egresoId: int) -> Egreso:
    egreso = db.session.query(Egreso).filter_by(id=egresoId).first()
    return egreso

def existeFactura(facturaId: int) -> Factura:
    factura = db.session.query(Factura).filter_by(id=facturaId).first()
    return factura