from condominioApi import db
from condominioApi.models import Cuenta, Recibo, Factura
from condominioApi.errors import APINotFound, APIBadRequest

def agregarIngreso(cuentaId, cantidad):
    cuenta = db.session.query(Cuenta).filter_by(id=cuentaId).first()
    if not cuenta:
        raise APINotFound('La cuenta no existe')
    try:
        cuenta.saldo += cantidad
    except:
        raise APIBadRequest
    return cuenta

def agregarEgreso(cuentaId, cantidad):
    cuenta = db.session.query(Cuenta).filter_by(id=cuentaId).first()
    if not cuenta:
        raise APINotFound('La cuenta no existe')
    try:
        cuenta.saldo -= cantidad
    except:
        raise APIBadRequest
    return cuenta

def actualizarSaldo(cantidadActualizada: float, recibo: Recibo=None, factura: Factura=None):
    if recibo and not factura:
        cuenta = db.session.query(Cuenta).filter_by(id=recibo.ingreso.cuenta_id).first()
        cuenta.saldo += cantidadActualizada - recibo.cantidad
    elif factura and not recibo:
        cuenta = db.session.query(Cuenta).filter_by(id=factura.egreso.cuenta_id).first()
        cuenta.saldo -= cantidadActualizada - factura.cantidad
    return cuenta