from app import db, ma
from sqlalchemy import Column, Integer, String, ForeignKey, Text

from .cliente import Cliente
from .empleado import Empleado

class Proyecto(db.Model):

    numero_proyecto = Column(Integer, primary_key=True, autoincrement=True)
    nombre_proyecto = Column(String(255), nullable=False)
    descripcion_proyecto = Column(Text, nullable=True)
    
    #RELACIONES
    cliente = Column(Integer, ForeignKey(Cliente.id_cliente))
    encargado_proyecto = Column(Integer, ForeignKey(Empleado.codigo_empleado))


    def __init__(self, nombre_proyecto, descripcion_proyecto, cliente, encargado_proyecto):
        
        self.nombre_proyecto = nombre_proyecto
        self.descripcion_proyecto = descripcion_proyecto
        self.cliente = cliente
        self.encargado_proyecto = encargado_proyecto

    def __repr__(self):
        return ""

class ProyectoSchema(ma.Schema):
    class Meta():
        fields = ('numero_proyecto','nombre_proyecto','descripcion_proyecto', 'cliente', 'encargado_proyecto')