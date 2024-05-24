from app import db, ma
from sqlalchemy import Column, ForeignKey, Integer, Date

class NotaDeEntrega(db.Model):

    __tablename__ = "notas_de_entrega"

    nro_nota = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date)

    nro_orden = Column(Integer, ForeignKey('ordenes_de_compra.nro_orden'))

    # Relación con OrdenDeCompra
    orden_de_compra = db.relationship('OrdenDeCompra', back_populates='notas_entrega')

    def __init__(self, nro_orden, fecha):
        self.nro_orden = nro_orden
        self.fecha = fecha


class NotaDeEntregaSchema(ma.Schema):
    class Meta():
        fields = ("nro_nota", "fecha", "nro_orden")