from app import db, ma
from sqlalchemy import Column, Date, Numeric, Text, ForeignKey, Integer


class FacturaOrdenCompra(db.Model):
    __tablename__ = "facturas_ordenes_de_compra"

    nro_factura = Column(Integer, primary_key=True, autoincrement=True)
    monto = Column(Numeric(8, 2))
    fecha = Column(Date)
    descripcion = Column(Text, nullable=True)

    # Claves foráneas
    nro_orden = Column(Integer, ForeignKey('ordenes_de_compra.nro_orden'))
    nro_proveedor = Column(Integer, ForeignKey('proveedores.nro_proveedor'))

    # Relaciones
    orden_de_compra = db.relationship('OrdenDeCompra', back_populates='factura')
    proveedor = db.relationship('Proveedor', back_populates='facturas')

    # Relación uno a uno con Deposito
    nro_deposito = Column(Integer, ForeignKey("depositos.nro_deposito"))
    deposito = db.relationship('Deposito', uselist=False, back_populates='factura_orden_compra')

    def __init__(self, nro_proveedor, monto, fecha, descripcion, nro_deposito):
        self.nro_proveedor = nro_proveedor
        self.fecha = fecha
        self.descripcion = descripcion
        self.monto = monto
        self.nro_deposito = nro_deposito

class FacturaOrdenCompraSchema(ma.Schema):
    class Meta():
        fields = ("nro_factura", "nro_proveedor", "monto", "fecha", "descripcion")