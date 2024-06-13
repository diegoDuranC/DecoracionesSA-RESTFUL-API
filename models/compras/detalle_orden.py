from app import db, ma
from sqlalchemy import Column, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship
from marshmallow import fields
from models.material.material import MaterialSchema

class DetalleOrdenCompra(db.Model):
    __tablename__ = "detalle_orden_de_compra"

    id = Column(Integer, autoincrement=True, primary_key=True)
    nro_orden = Column(Integer, ForeignKey("ordenes_de_compra.nro_orden"))
    id_material = Column(Integer, ForeignKey("materiales.ID_material"))
    cantidad_requerida = Column(Integer)
    precio_material = Column(Numeric(8, 2))

    # RELACIONES
    orden = relationship('OrdenDeCompra', back_populates='detalles')
    material = relationship('Material', back_populates='detalles')

    def __init__(self, cantidad_requerida, precio_material, id_material, nro_orden):
        self.cantidad_requerida = cantidad_requerida
        self.precio_material = precio_material
        self.id_material = id_material
        self.nro_orden = nro_orden

class DetalleOrdenCompraSchema(ma.Schema):
    material = fields.Nested(MaterialSchema, exclude=('ID_material',))
    class Meta:
        fields = ("id", "nro_orden", "id_material", "cantidad_requerida", "precio_material", "material")
