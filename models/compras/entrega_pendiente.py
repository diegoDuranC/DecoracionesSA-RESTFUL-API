from datetime import datetime
from enum import Enum
from app import db, ma
from sqlalchemy import Column, Date, Integer, ForeignKey, Enum as SqlEnum, String
from marshmallow import fields

from models.compras.detalle_material_pendiente import DetalleMaterialPendienteSchema

class EstadoEntrega(Enum):
    PENDIENTE = "PENDIENTE"
    ENTREGADO = "ENTREGADO"

class EntregaPendiente(db.Model):
    __tablename__ = "entregas_pendientes"

    id_entrega_pendiente = Column(Integer, primary_key=True, autoincrement=True)
    fecha_creacion = Column(Date)
    fecha_actualizacion = Column(Date)
    estado = Column(SqlEnum(EstadoEntrega), default=EstadoEntrega.PENDIENTE)

    # Relaciones
    #Relacion con Nota Entrega
    nro_nota = Column(Integer, ForeignKey('notas_de_entrega.nro_nota'))
    nota_de_entrega = db.relationship('NotaDeEntrega', back_populates='entregas_pendientes')

    #Relacion con Detalle
    detalles_materiales_pendientes = db.relationship('DetalleMaterialPendiente', back_populates='entrega_pendiente')
    materiales_recibidos = db.relationship('MaterialRecibido', back_populates='entrega_pendiente')
     
    def __init__(self, fecha_actualizacion, nro_nota, estado=EstadoEntrega.PENDIENTE):
        self.nro_nota = nro_nota
        self.estado = estado
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d")
        self.fecha_actualizacion = fecha_actualizacion

class EntregaPendienteSchema(ma.Schema):
    estado = fields.Method("get_estado")
    detalles_materiales_pendientes = fields.List(fields.Nested(DetalleMaterialPendienteSchema, exclude=("entrega_pendiente_id",)))
    class Meta:
        model = EntregaPendiente
        fields = ("fecha_creacion", "fecha_actualizacion", "estado", "nro_nota", "id_entrega_pendiente", "detalles_materiales_pendientes")
        include_fk = True

    def get_estado(self, obj):
        return obj.estado.value