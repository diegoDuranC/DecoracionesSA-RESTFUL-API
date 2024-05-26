from datetime import datetime
from app import db, ma
from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from marshmallow import fields

class TransaccionInventario(db.Model):
    __tablename__ = 'transacciones_inventario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_transaccion = Column(String(20), unique=True, nullable=False)
    codigo_material = Column(Integer, ForeignKey('materiales.codigo_material'))
    descripcion = Column(String(255), nullable=False)
    precio_unitario = Column(Float, nullable=False)
    fecha_transaccion = Column(Date, default=datetime.utcnow)
    cantidad_entrada = Column(Float, nullable=True)
    cantidad_salida = Column(Float, nullable=True)
    existencia_salida = Column(Float, nullable=False)

    material = db.relationship('Material', back_populates='transacciones_inventario')

    def __init__(self, codigo_transaccion, codigo_material, descripcion, precio_unitario, fecha_transaccion, cantidad_entrada, cantidad_salida, existencia_salida):
        self.codigo_transaccion = codigo_transaccion
        self.codigo_material = codigo_material
        self.descripcion = descripcion
        self.precio_unitario = precio_unitario
        self.fecha_transaccion = fecha_transaccion
        self.cantidad_entrada = cantidad_entrada
        self.cantidad_salida = cantidad_salida
        self.existencia_salida = existencia_salida

class TransaccionInventarioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TransaccionInventario
        fields = ("id", "codigo_transaccion", "codigo_material", "descripcion", "precio_unitario", "fecha_transaccion", "cantidad_entrada", "cantidad_salida", "existencia_salida")
