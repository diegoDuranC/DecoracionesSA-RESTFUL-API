from datetime import datetime
from app import db, ma
from sqlalchemy import Column, ForeignKey, Integer, Date
from marshmallow import fields

class NotaDeEntrega(db.Model):
    __tablename__ = "notas_de_entrega"

    nro_nota = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, default=datetime.now().strftime("%Y-%m-%d"))

    # Relación con OrdenDeCompra
    nro_orden = Column(Integer, ForeignKey('ordenes_de_compra.nro_orden'))
    orden_de_compra = db.relationship('OrdenDeCompra', back_populates='notas_entrega')

    materiales_recibidos = db.relationship('MaterialRecibido', back_populates='nota_de_entrega')

    def __init__(self, nro_orden):
        self.nro_orden = nro_orden

class NotaDeEntregaSchema(ma.Schema):
    materiales_recibidos = fields.List(fields.Nested('MaterialRecibidoSchema', exclude=('nro_nota',)))
    class Meta:
        fields = ("nro_nota", "fecha", "nro_orden", "materiales_recibidos")
