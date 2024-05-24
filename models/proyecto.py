from app import db, ma
from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, Text
from .rrhh.empleado import EmpleadoRequisicionSchema, EmpleadoSchema
from .cliente.cliente import ClienteSchema
from marshmallow_sqlalchemy import fields

class Proyecto(db.Model):
    
    __tablename__ = "proyectos"

    numero_proyecto = Column(Integer, primary_key=True, autoincrement=True)
    nombre_proyecto = Column(String(255), nullable=False)
    descripcion_proyecto = Column(Text, nullable=True)
    
    #LLAVES FORANEAS Y RELACIONES
    encargado_proyecto = Column(Integer, ForeignKey("empleados.codigo_empleado"))
    encargado = db.relationship('Empleado', back_populates='proyectos')

    cliente_id = Column(Integer, ForeignKey("clientes.id_cliente"))
    cliente = db.relationship('Cliente', back_populates='proyectos')

    requisiciones = db.relationship('Requisicion', back_populates='proyecto')
    
    factura = db.relationship('FacturaCliente', uselist=False, back_populates='proyecto')

    recibos = db.relationship('Recibo', back_populates='proyecto')

    def __init__(self, nombre_proyecto, descripcion_proyecto, cliente_id, encargado_proyecto):      
        self.nombre_proyecto = nombre_proyecto
        self.descripcion_proyecto = descripcion_proyecto
        self.cliente_id = cliente_id
        self.encargado_proyecto = encargado_proyecto

    def __repr__(self):
        return f'<Proyecto {self.nombre_proyecto}>'


class ProyectoSchema(ma.Schema): 
    encargado = ma.Nested(EmpleadoSchema, only=('nombre_empleado', 'apellido_empleado'))
    cliente = ma.Nested(ClienteSchema,only=('id_cliente', 'nombre_cliente', 'apellido_cliente'))

    class Meta():
        fields = ('numero_proyecto','nombre_proyecto','descripcion_proyecto', 'cliente', 'encargado')

class ProyectoRequisicionSchema(ma.Schema):
    encargado = fields.Nested(EmpleadoRequisicionSchema)
    cliente = fields.Nested(ClienteSchema, only=('nombre_cliente', 'apellido_cliente', 'telefono_cliente', 'direccion_cliente'))

    class Meta():
        fields = ('numero_proyecto','nombre_proyecto','descripcion_proyecto', 'cliente', 'encargado')

class ProyectoFacturaSchema(ma.Schema):
    encargado = fields.Nested(EmpleadoRequisicionSchema)
    class Meta:
        fields = ('encargado',)