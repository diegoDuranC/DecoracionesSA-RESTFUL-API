from app import db, ma
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from datetime import datetime

from .proyecto import Proyecto

class Requisicion(db.Model):
    __tablename__ = "requisiciones"

    nro_requisicion = Column(Integer, autoincrement=True, primary_key=True)
    fecha_creacion = Column(Date)
    fecha_entrega_requerida = Column(Date, nullable=False)
    descripcion = Column(Text, nullable=True)
    estado = Column(String(15), nullable=False)

    #Relacion
    proyecto = Column(Integer, ForeignKey(Proyecto.numero_proyecto))

    def __init__ (self, fecha_entrega_requerida, descripcion, estado, proyecto):
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d")
        self.fecha_entrega_requerida = fecha_entrega_requerida
        self.descripcion = descripcion
        self.estado = estado.lower()
        self.proyecto = proyecto


class RequisicionSchema(ma.Schema):
    class Meta():
        fields = ('nro_requisicion', 'fecha_creacion', 'fecha_entrega', 'descripcion', 'estado', 'proyecto')