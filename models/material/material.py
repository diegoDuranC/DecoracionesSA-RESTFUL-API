from app import db, ma
from sqlalchemy import Column, Integer, Float, String

class Material(db.Model):
    __tablename__ = 'materiales'

    codigo_material = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(255), nullable=False)
    existencias = Column(Float, nullable=False)
    precio_unitario = Column(Float)

    # RELACIONES
    detalles = db.relationship('DetalleOrdenCompra', back_populates='material')  # Relación definida

    # Relación con la tabla asociativa Requisicion
    requisiciones = db.relationship('DetalleMaterialRequisicion', back_populates='material')

    #Asociacion con materiales recibidos
    materiales_recibidos = db.relationship('MaterialRecibido', back_populates='material')

    #relacion con transacciones
    transacciones_inventario = db.relationship('TransaccionInventario', back_populates='material')

    def __init__(self, descripcion, precio_unitario, existencias):
        self.descripcion = descripcion
        self.precio_unitario = precio_unitario
        self.existencias = existencias

    def __repr__(self):
        return '<Material %r>' % self.descripcion

class MaterialSchema(ma.Schema):
    class Meta:
        fields = ('codigo_material', 'descripcion', 'precio_unitario', 'existencias')

class MaterialRequisicionSchema(ma.Schema):
    class Meta:
        fields = ('descripcion', 'precio_unitario')