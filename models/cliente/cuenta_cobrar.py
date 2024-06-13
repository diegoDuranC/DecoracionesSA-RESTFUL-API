from app import db,ma
from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, Numeric, Date
from marshmallow import fields

from models.cliente.cliente import ClienteFacturaSchema
from models.cliente.factura_cliente import FacturaSchema

from models.cliente.plan_pago_cliente import PlanPagoClienteSchema

class CuentaPorCobrar(db.Model):
    __tablename__ = "cuentas_por_cobrar"

    nro_cuenta = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey("clientes.ID_cliente"))
    importe = Column(Numeric(8,2))
    saldo = Column(Numeric(8,2))
    fecha_creacion = Column(Date)
    vencimiento = Column(Date)
    amortizacion = Column(SmallInteger, default=1)

    cliente = db.relationship('Cliente', back_populates='cuentas_por_cobrar')
    pagos = db.relationship('PlanPagoCliente', back_populates='cuenta')
    recibos = db.relationship("Recibo", back_populates="cuenta_por_cobrar")

    nro_factura = Column(Integer, ForeignKey("facturas_cliente.nro_factura"))
    factura = db.relationship('FacturaCliente', back_populates="cuenta_por_cobrar")

    def __init__(self, importe, saldo, id_cliente, fecha_creacion, nro_factura):
        self.importe = importe
        self.saldo = saldo
        self.fecha_creacion = fecha_creacion
        self.id_cliente = id_cliente
        self.nro_factura = nro_factura

class CuentaPorCobrarSchema(ma.Schema):
    cliente = fields.Nested(ClienteFacturaSchema)
    factura = fields.Nested(FacturaSchema, only=("nro_factura", "fecha", "total"))
    pagos = fields.List(fields.Nested(PlanPagoClienteSchema))
    class Meta():
        fields = ("nro_cuenta", "importe", "saldo", "vencimiento", "amortizacion", "fecha_creacion", "cliente", "factura", "pagos")


class EstadoCuentaSchema(ma.Schema):
    cliente = fields.Nested(ClienteFacturaSchema)
    factura = fields.Nested(FacturaSchema, only=("nro_factura", "fecha", "total"))
    pagos = fields.List(fields.Nested(PlanPagoClienteSchema))
    class Meta():
        fields = ("saldo", "cliente", "factura", "pagos")

class CuentaPorCobrarRecibo(ma.Schema):
    factura = fields.Nested(FacturaSchema, only=("nro_factura",))
    class Meta():
        fields = ("nro_cuenta",)