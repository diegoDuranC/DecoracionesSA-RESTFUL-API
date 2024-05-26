from app import ma, db
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric, Enum as SqlEnum
from marshmallow import fields
from enum import Enum 

class FormaPago(Enum):
    EFECTIVO = "EFECTIVO"
    CHEQUE = "CHEQUE"
    TRANSFERENCIA = "TRANSFERENCIA"

class Deposito(db.Model):
    
    __tablename__ = 'depositos'

    nro_deposito = Column(Integer, primary_key=True, autoincrement=True)
    cuenta = Column(String(15), nullable=False)
    fecha = Column(Date)
    monto = Column(Numeric(8,2))

    banco_id = Column(Integer, ForeignKey("bancos.id_banco"))
    banco = db.relationship('Banco', back_populates='depositos')
    forma_pago = Column(SqlEnum(FormaPago), nullable=False)

    empleado_id = Column(Integer, ForeignKey("empleados.codigo_empleado"))
    empleado = db.relationship('Empleado', back_populates='depositos')

    # Relación uno a uno con Recibo
    recibo = db.relationship('Recibo', uselist=False, back_populates='deposito')

    # Relación uno a uno con FacturaOrdenCompra
    factura_orden_compra = db.relationship('FacturaOrdenCompra', uselist=False, back_populates='deposito')

    def __init__(self, cuenta, fecha, monto, banco_id, forma_pago):
        self.cuenta = cuenta
        self.fecha = fecha
        self.monto = monto
        self.banco_id = banco_id
        self.forma_pago = forma_pago

class DepositoSchema(ma.Schema):
    forma_pago = fields.Method("get_forma_pago")
    class Meta():
        fields = ("nro_deposito", "cuenta", "monto", "fecha", "banco_id", "forma_pago")

    def get_forma_pago(self,obj):
        return obj.forma_pago.value