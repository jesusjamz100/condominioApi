from marshmallow import Schema, fields

# Se crean los schemas para la serializacion de datos desde la base de datos
# para retornar el json sin problemas
class ApartamentoSchema(Schema):
    id = fields.Int(dump_only=True)
    propietario_id = fields.Int()
    piso_id = fields.Int()
    codigo = fields.String()

class PisoSchema(Schema):
    id = fields.Int(dump_only=True)
    torre_id = fields.Int()
    numero = fields.Int()
    apartamentos = fields.List(fields.Nested(ApartamentoSchema))

class TorreSchema(Schema):
    id = fields.Int(dump_only=True)
    letra = fields.Str()
    pisos = fields.List(fields.Nested(PisoSchema))

class ReciboSchema(Schema):
    id = fields.Int(dump_only=True)
    propietario_id = fields.Int()
    ingreso_id = fields.Int()
    cantidad = fields.Float()
    fecha = fields.Date()

class IngresoSchema(Schema):
    id = fields.Int(dump_only=True)
    cuenta_id = fields.Int()
    descripcion = fields.Str()
    recibo = fields.Nested(ReciboSchema)

class PropietarioSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str()
    apellido = fields.Str()
    email = fields.Email()
    apartamentos = fields.List(fields.Nested(ApartamentoSchema))
    recibos = fields.List(fields.Nested(ReciboSchema))

class FacturaSchema(Schema):
    id = fields.Int(dump_only=True)
    egreso_id = fields.Int()
    cantidad = fields.Float()
    fecha = fields.Date()

class EgresoSchema(Schema):
    id = fields.Int(dump_only=True)
    cuenta_id = fields.Int()
    descripcion = fields.Str()
    factura = fields.Nested(FacturaSchema)

class CuentaSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str()
    saldo = fields.Float()
    ingresos = fields.List(fields.Nested(IngresoSchema))
    egresos = fields.List(fields.Nested(EgresoSchema))