from app import db, ma
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Float
from datetime import datetime

from .proyecto import Proyecto
from .material import Material

#ENTIDAD ASOCIATIVA ENTRE MATERIALES Y REQUISICION
'''
    ESPECIFICA EN CADA REGISTRO LA CANTIDAD QUE SE SOLICITO DE MATERIAL PARA LA REQUISICION
    AL SER UN CAMPO MULTIVALUADO
'''

detalleMaterialSolicitado = db.Table(
    "detalleMaterialSolicitado-MaterialRequisicion",
    Column("id",Integer, autoincrement=True, primary_key=True),
    Column("cantidad_solicitada", Float),
    Column("nro_requisicion",Integer, ForeignKey("requisiciones.nro_requisicion")),
    Column("codigo_material", Integer, ForeignKey("materiales.codigo_material"))
)

class Requisicion(db.Model):
    __tablename__ = "requisiciones"

    nro_requisicion = Column(Integer, autoincrement=True, primary_key=True)
    fecha_creacion = Column(Date)
    fecha_entrega_requerida = Column(Date, nullable=False)
    descripcion = Column(Text, nullable=True)
    estado = Column(String(15), nullable=False)

    #Relacion
    proyecto = Column(Integer, ForeignKey(Proyecto.numero_proyecto))

    materiales_solicitados = db.relationship("Material", secondary=detalleMaterialSolicitado, backref="requisiciones")

    def __init__ (self, fecha_entrega_requerida, descripcion, estado, proyecto):
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d")
        self.fecha_entrega_requerida = fecha_entrega_requerida
        self.descripcion = descripcion
        self.estado = estado.lower()
        self.proyecto = proyecto

class RequisicionSchema(ma.Schema):
    class Meta():
        fields = ('nro_requisicion', 'fecha_creacion', 'fecha_entrega', 'descripcion', 'estado', 'proyecto')

class DetalleMaterialSolicitadoSchema(ma.Schema):
    class Meta():
        fields = ("id", "cantidad_solicitada", "nro_requisicion", "codigo_material")