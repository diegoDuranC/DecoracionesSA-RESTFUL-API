from app import db, ma
from sqlalchemy import Column, Integer, Numeric, Date, Text, ForeignKey
from marshmallow import fields
from datetime import datetime
from .detalle_materiales import DetalleMaterialSolicitadoSchema
from models.cliente.cliente import ClienteSchema

from models.proyecto import ProyectoSchema, ProyectoRequisicionSchema

class Requisicion(db.Model):
    __tablename__ = "requisiciones"

    nro_requisicion = Column(Integer, autoincrement=True, primary_key=True)
    fecha_creacion = Column(Date)
    fecha_entrega_requerida = Column(Date, nullable=False)
    descripcion = Column(Text, nullable=True)
    costo = Column(Numeric(8,2))

    # Relación con Proyecto
    proyecto_id = Column(Integer, ForeignKey("proyectos.numero_proyecto"))
    proyecto = db.relationship('Proyecto', back_populates='requisiciones')

    # Relación con la tabla Material a través de la tabla asociativa
    materiales_solicitados = db.relationship("DetalleMaterialRequisicion", back_populates="requisicion")

    def __init__ (self, fecha_entrega_requerida, descripcion, proyecto_id, costo):
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d")
        self.fecha_entrega_requerida = fecha_entrega_requerida
        self.descripcion = descripcion
        self.proyecto_id = proyecto_id
        self.costo = costo

class RequisicionSchema(ma.Schema):
    proyecto = fields.Nested(ProyectoRequisicionSchema)
    materiales_solicitados = fields.List(fields.Nested(DetalleMaterialSolicitadoSchema, exclude=('nro_requisicion',)))

    class Meta():
        model = Requisicion 
        fields = ('nro_requisicion', 'fecha_creacion', 'fecha_entrega_requerida', 'descripcion', 'proyecto', 'cliente', 'materiales_solicitados', 'costo')

class SingleRequisicionSchema(ma.Schema):
    class Meta():
        fields = ('nro_requisicion', 'fecha_creacion', 'fecha_entrega_requerida', 'descripcion', 'costo')
