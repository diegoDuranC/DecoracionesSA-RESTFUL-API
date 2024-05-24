from app import db, ma
from sqlalchemy import Column, ForeignKey, Integer, Numeric

class DetalleOrdenCompra(db.Model):
    __tablename__ = "detalle_orden_de_compra"

    nro_orden = Column(Integer, ForeignKey("ordenes_de_compra.nro_orden"), primary_key=True)
    codigo_material = Column(Integer, ForeignKey("materiales.codigo_material"), primary_key=True)
    cantidad_requerida = Column(Integer)
    precio_material = Column(Numeric(8, 2))

    # RELACIONES
    orden = db.relationship('OrdenDeCompra', back_populates='detalles')  # Relación definida
    material = db.relationship('Material', back_populates='detalles')  # Relación definida

    def __init__(self, cantidad_requerida, precio_material, codigo_material, nro_orden):
        self.cantidad_requerida = cantidad_requerida
        self.precio_material = precio_material
        self.codigo_material = codigo_material
        self.nro_orden = nro_orden

class DetalleOrdenCompraSchema(ma.Schema):
    class Meta:
        fields = ("nro_orden", "codigo_material", "cantidad_requerida", "precio_material")
