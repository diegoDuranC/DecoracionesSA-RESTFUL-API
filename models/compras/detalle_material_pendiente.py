# from app import db, ma
# from sqlalchemy import Column, Integer, Float, String, ForeignKey

# class DetalleMaterialPendiente(db.Model):
#     __tablename__ = "detalles_materiales_pendientes"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     cod_material = Column(Integer, ForeignKey('materiales.codigo_material'))
#     cantidad_pendiente = Column(Float)
#     descripcion = Column(String(80))
    
#     # Relaciones
#     entrega_pendiente_id = Column(Integer, ForeignKey('entregas_pendientes.id_entrega_pendiente'))
#     entrega_pendiente = db.relationship('EntregaPendiente', back_populates='detalles_materiales_pendientes')

#     def __init__(self, cod_material, cantidad_pendiente, descripcion, entrega_pendiente_id):
#         self.cod_material = cod_material
#         self.cantidad_pendiente = cantidad_pendiente
#         self.descripcion = descripcion
#         self.entrega_pendiente_id = entrega_pendiente_id

# class DetalleMaterialPendienteSchema(ma.Schema):
#     class Meta:
#         model = DetalleMaterialPendiente
#         fields = ("cod_material", "cantidad_pendiente", "descripcion", "entrega_pendiente_id")
