# from datetime import datetime
# from app import db, ma
# from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
# from marshmallow import fields

# class TransaccionInventario(db.Model):
#     __tablename__ = 'transacciones_inventario'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     codigo_transaccion = Column(String(20), unique=True, nullable=False)
#     id_material = Column(Integer, ForeignKey('materiales.ID_material'))
#     descripcion = Column(String(255), nullable=False)
#     precio_unitario = Column(Float, nullable=False)
#     fecha_transaccion = Column(Date, default=datetime.now().strftime("%Y-%m-%d"))
#     cantidad_entrada = Column(Float, nullable=True)
#     cantidad_salida = Column(Float, nullable=True)
#     existencia_salida = Column(Float, nullable=False)

#     material = db.relationship('Material', back_populates='transacciones_inventario')

#     detalle_material_id = Column(Integer, ForeignKey("detalle_materiales_requisicion.ID"))
#     detalle_material = db.relationship('DetalleMaterialRequisicion', back_populates='transaccion', uselist=False)

#     material_recibido_id = Column(Integer, ForeignKey("materiales_recibidos.id"))
#     material_recibido = db.relationship('MaterialRecibido', back_populates="transaccion", uselist=False)

#     # # material_recibido_id = Column(Integer, ForeignKey("materiales_recibidos.id"))
#     # # material_recibido = db.relationship('MaterialRecibido', back_populates='')

#     def __init__(self, codigo_transaccion, id_material, descripcion, precio_unitario, fecha_transaccion, cantidad_entrada, cantidad_salida, existencia_salida, detalle_id=None, material_recibido_id=None):
#         self.codigo_transaccion = codigo_transaccion
#         self.id_material = id_material
#         self.descripcion = descripcion
#         self.precio_unitario = precio_unitario
#         self.fecha_transaccion = fecha_transaccion
#         self.cantidad_entrada = cantidad_entrada
#         self.cantidad_salida = cantidad_salida
#         self.existencia_salida = existencia_salida
#         self.detalle_id = detalle_id
#         self.material_recibido_id = material_recibido_id

# class TransaccionInventarioSchema(ma.SQLAlchemySchema):
#     class Meta:
#         model = TransaccionInventario
#         fields = (
#             "id", 
#             "codigo_transaccion", 
#             "id_material", 
#             "descripcion", 
#             "precio_unitario", 
#             "fecha_transaccion", 
#             "cantidad_entrada", 
#             "cantidad_salida", 
#             "existencia_salida",
#             "material_recibido_id",
#             "detalle_material_id"
#         )

from datetime import datetime
from app import db, ma
from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from marshmallow import fields

class TransaccionInventario(db.Model):
    __tablename__ = 'transacciones_inventario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_transaccion = Column(String(20), unique=True, nullable=False)
    id_material = Column(Integer, ForeignKey('materiales.ID_material'))
    descripcion = Column(String(255), nullable=False)
    precio_unitario = Column(Float, nullable=False)
    fecha_transaccion = Column(Date, default=datetime.now().strftime("%Y-%m-%d"))
    cantidad_entrada = Column(Float, nullable=True)
    cantidad_salida = Column(Float, nullable=True)
    existencia_salida = Column(Float, nullable=False)

    material = db.relationship('Material', back_populates='transacciones_inventario')

    detalle_material_id = Column(Integer, ForeignKey("detalle_materiales_requisicion.ID"))
    detalle_material = db.relationship('DetalleMaterialRequisicion', back_populates='transaccion', uselist=False)

    material_recibido_id = Column(Integer, ForeignKey("materiales_recibidos.id"))
    material_recibido = db.relationship('MaterialRecibido', back_populates="transaccion", uselist=False)

    def __init__(self, codigo_transaccion, fecha_transaccion, id_material, descripcion, precio_unitario, cantidad_entrada, cantidad_salida, existencia_salida, detalle_material_id=None, material_recibido_id=None):
        self.codigo_transaccion = codigo_transaccion
        self.fecha_transaccion = fecha_transaccion
        self.id_material = id_material
        self.descripcion = descripcion
        self.precio_unitario = precio_unitario
        self.cantidad_entrada = cantidad_entrada
        self.cantidad_salida = cantidad_salida
        self.existencia_salida = existencia_salida
        self.detalle_material_id = detalle_material_id
        self.material_recibido_id = material_recibido_id

class TransaccionInventarioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TransaccionInventario
        fields = (
            "id", 
            "codigo_transaccion", 
            "id_material", 
            "descripcion", 
            "precio_unitario", 
            "fecha_transaccion", 
            "cantidad_entrada", 
            "cantidad_salida", 
            "existencia_salida",
            "material_recibido_id",
            "detalle_material_id"
        )

