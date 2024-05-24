'''
    MODELO QUE REPRESENTA LA ORDEN DE COMPRA DE MATERIAL A UN PROVEEDOR, INCLUYE LA TABLA ASOCIATIVA RESULTANTE DE LA RELACIÓN MUCHOS A MUCHOS CON MATERIAL,
    JUNTO CON LA ENTIDAD DÉBIL DE LA NOTA DE ENTREGA DEL MATERIAL SOLICITADO, POR PARTE DEL PROVEEDOR Y LA FACTURA QUE SE GENERA POR LA COMPRA DE DICHA ORDEN
'''

from app import db, ma
from sqlalchemy import Column, Integer, Text, Date
from datetime import datetime
from marshmallow import fields

from models.compras.detalle_orden import DetalleOrdenCompraSchema

class OrdenDeCompra(db.Model):
    __tablename__ = "ordenes_de_compra"

    nro_orden = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date)
    descripcion = Column(Text, nullable=True)

    # RELACIONES
    factura = db.relationship('FacturaOrdenCompra', back_populates='orden_de_compra', uselist=False)
    notas_entrega = db.relationship('NotaDeEntrega', back_populates='orden_de_compra')
    detalles = db.relationship('DetalleOrdenCompra', back_populates='orden')  # Relación definida

    def __init__(self, descripcion):
        self.fecha = datetime.now().strftime("%Y-%m-%d")
        self.descripcion = descripcion

class OrdenDeCompraSchema(ma.Schema):
    detalles = fields.List(fields.Nested(DetalleOrdenCompraSchema, exclude=("nro_orden",)))
    class Meta:
        fields = ("nro_orden", "fecha", "descripcion", "detalles")