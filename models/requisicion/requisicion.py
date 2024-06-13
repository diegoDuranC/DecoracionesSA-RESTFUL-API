# from app import db, ma
# from sqlalchemy import Column, Integer, Numeric, Date, Text, ForeignKey, String
# from marshmallow import fields
# from datetime import datetime
# from .detalle_materiales import DetalleMaterialSolicitadoSchema
# from models.cliente.cliente import ClienteSchema

# from models.proyecto import ProyectoSchema, ProyectoRequisicionSchema

# class Requisicion(db.Model):
#     __tablename__ = "requisiciones"

#     nro_requisicion = Column(Integer, autoincrement=True, primary_key=True)
#     fecha_creacion = Column(Date)
#     fecha_entrega_requerida = Column(Date, nullable=False)
#     descripcion = Column(Text, nullable=True)
#     costo = Column(Numeric(8,2))

#     # Relación con Proyecto
#     proyecto_nro_proyecto = Column(Integer, ForeignKey("proyectos.nro_proyecto"))
#     proyecto = db.relationship('Proyecto', back_populates='requisiciones')

#     # Relación con la tabla Material a través de la tabla asociativa
#     materiales_solicitados = db.relationship("DetalleMaterialRequisicion", back_populates="requisicion")

#     def __init__ (self, fecha_entrega_requerida, descripcion, proyecto_nro_proyecto, costo):
#         self.fecha_creacion = datetime.now().strftime("%Y-%m-%d")
#         self.fecha_entrega_requerida = fecha_entrega_requerida
#         self.descripcion = descripcion
#         self.proyecto_nro_proyecto = proyecto_nro_proyecto
#         self.costo = costo

# class RequisicionSchema(ma.Schema):
#     proyecto = fields.Nested(ProyectoRequisicionSchema)
#     materiales_solicitados = fields.List(fields.Nested(DetalleMaterialSolicitadoSchema, exclude=('nro_requisicion',)))

#     class Meta():
#         model = Requisicion 
#         fields = ('nro_requisicion', 'fecha_creacion', 'fecha_entrega_requerida', 'descripcion', 'costo', 'proyecto', 'materiales_solicitados')

# class SingleRequisicionSchema(ma.Schema):
#     class Meta():
#         fields = ('nro_requisicion', 'fecha_creacion', 'fecha_entrega_requerida', 'descripcion', 'costo')

from app import db, ma
from sqlalchemy import Column, Integer, Numeric, Date, Text, ForeignKey, String
from datetime import datetime
from marshmallow import fields
from models.cliente.cliente import ClienteSchema
from models.proyecto import ProyectoSchema, ProyectoRequisicionSchema

class Requisicion(db.Model):
    __tablename__ = "requisiciones"

    nro_requisicion = Column(Integer, autoincrement=True, primary_key=True)
    fecha_creacion = Column(Date, default=datetime.now().strftime("%Y-%m-%d"))
    fecha_entrega_requerida = Column(Date, nullable=False)
    descripcion = Column(Text, nullable=True)
    costo = Column(Numeric(8, 2))

    # Relación con Proyecto
    proyecto_nro_proyecto = Column(Integer, ForeignKey("proyectos.nro_proyecto"))
    proyecto = db.relationship('Proyecto', back_populates='requisiciones')

    # Relación con la tabla Material a través de la tabla asociativa
    materiales_solicitados = db.relationship("DetalleMaterialRequisicion", back_populates="requisicion")

    def __init__(self, fecha_entrega_requerida, descripcion, proyecto_nro_proyecto, costo):
        self.fecha_entrega_requerida = fecha_entrega_requerida
        self.descripcion = descripcion
        self.proyecto_nro_proyecto = proyecto_nro_proyecto
        self.costo = costo

class RequisicionSchema(ma.Schema):
    proyecto = fields.Nested(ProyectoRequisicionSchema)
    materiales_solicitados = fields.List(fields.Nested('DetalleMaterialSolicitadoSchema', exclude=('nro_requisicion',)))

    class Meta:
        model = Requisicion
        fields = ('nro_requisicion', 'fecha_creacion', 'fecha_entrega_requerida', 'descripcion', 'costo', 'proyecto', 'materiales_solicitados')

class SingleRequisicionSchema(ma.Schema):
    class Meta:
        fields = ('nro_requisicion', 'fecha_creacion', 'fecha_entrega_requerida', 'descripcion', 'costo')
