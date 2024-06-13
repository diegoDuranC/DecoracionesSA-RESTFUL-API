# from app import db,ma
# from sqlalchemy import Column, Integer, ForeignKey, Float
# from sqlalchemy.orm import relationship
# from marshmallow_sqlalchemy import fields

# from models.material.material import MaterialRequisicionSchema

# #ENTIDAD ASOCIATIVA ENTRE MATERIALES Y REQUISICION
# '''
#     ESPECIFICA EN CADA REGISTRO LA CANTIDAD QUE SE SOLICITO DE MATERIAL PARA LA REQUISICION
#     AL SER UN CAMPO MULTIVALUADO
# '''

# class DetalleMaterialRequisicion(db.Model):
#     __tablename__ = 'detalle_materiales_requisicion'

#     ID = Column(Integer, primary_key=True, autoincrement=True)
#     cantidad_solicitada = Column(Float)

#     nro_requisicion = Column(Integer, ForeignKey("requisiciones.nro_requisicion"))
#     id_material = Column(Integer, ForeignKey("materiales.ID_material"))

#     # Relaciones inversas
#     requisicion = relationship('Requisicion', back_populates='materiales_solicitados')
#     material = relationship('Material', back_populates='requisiciones')

#     transaccion = relationship('TransaccionInventario', back_populates='detalle_material', uselist=False)

#     def __init__(self, cantidad_solicitada, nro_requisicion, id_material):
#         self.cantidad_solicitada = cantidad_solicitada
#         self.nro_requisicion = nro_requisicion
#         self.id_material = id_material

# class DetalleMaterialSolicitadoSchema(ma.Schema):
#     material = fields.Nested(MaterialRequisicionSchema, exclude=('ID_material',))

#     class Meta():
#         fields = ("ID", "cantidad_solicitada", "nro_requisicion", "codigo_material", "material")

from app import db, ma
from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from marshmallow_sqlalchemy import fields

class DetalleMaterialRequisicion(db.Model):
    __tablename__ = 'detalle_materiales_requisicion'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    cantidad_solicitada = Column(Float)

    nro_requisicion = Column(Integer, ForeignKey("requisiciones.nro_requisicion"))
    id_material = Column(Integer, ForeignKey("materiales.ID_material"))

    # Relaciones inversas
    requisicion = relationship('Requisicion', back_populates='materiales_solicitados')
    material = relationship('Material', back_populates='requisiciones')
    transaccion = relationship('TransaccionInventario', back_populates='detalle_material', uselist=False)

    def __init__(self, cantidad_solicitada, nro_requisicion, id_material):
        self.cantidad_solicitada = cantidad_solicitada
        self.nro_requisicion = nro_requisicion
        self.id_material = id_material

class DetalleMaterialSolicitadoSchema(ma.Schema):
    material = fields.Nested('MaterialRequisicionSchema', exclude=('ID_material',))

    class Meta:
        fields = ("ID", "cantidad_solicitada", "nro_requisicion", "id_material", "material")
