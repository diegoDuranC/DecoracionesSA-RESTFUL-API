from app import db, ma
from sqlalchemy import Column, Integer, Text, Date, String, Enum as SqlEnum
from datetime import datetime
from enum import Enum
from marshmallow import fields

class EstadoCompra(Enum):
    SATISFECHA = "SATISFECHA"
    PENDIENTE = "PENDIENTE"
    CANCELADA = "CANCELADA"
    EN_PROCESO = "EN_PROCESO"
    PARCIALMENTE_SATISFECHA = "PARCIALMENTE_SATISFECHA"
    RECHAZADA = "RECHAZADA"

class OrdenDeCompra(db.Model):
    __tablename__ = "ordenes_de_compra"

    nro_orden = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(Text(255), nullable=False)
    cod_orden = Column(String(20), nullable=False)
    estado_compra = Column(SqlEnum(EstadoCompra), default=EstadoCompra.PENDIENTE, nullable=False)
    fecha = Column(Date, default=datetime.now().strftime("%Y-%m-%d"))

    # RELACIONES
    factura = db.relationship('FacturaOrdenCompra', back_populates='orden_de_compra', uselist=False)
    notas_entrega = db.relationship('NotaDeEntrega', back_populates='orden_de_compra')
    detalles = db.relationship('DetalleOrdenCompra', back_populates='orden')

    def __init__(self, descripcion, cod_orden, fecha=datetime.now().strftime("%Y-%m-%d")):
        self.descripcion = descripcion
        self.cod_orden = cod_orden
        self.fecha = fecha

class OrdenDeCompraSchema(ma.Schema):
    detalles = fields.List(fields.Nested('DetalleOrdenCompraSchema', exclude=("nro_orden",)))
    estado_compra = fields.Method("get_estado_compra")
    
    class Meta:
        fields = ("nro_orden", "cod_orden", "fecha", "detalles", "descripcion", "estado_compra")

    def get_estado_compra(self,obj):
        return obj.estado_compra.value
