from app import db, ma
from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, Text
from .rrhh.empleado import EmpleadoRequisicionSchema, EmpleadoSchema
from .cliente.cliente import ClienteSchema
from marshmallow import fields

class Proyecto(db.Model):
    
    __tablename__ = "proyectos"

    nro_proyecto = Column(Integer, primary_key=True, autoincrement=True)
    cod_proyecto = Column(String(20), nullable=False)
    nombre_proyecto = Column(String(255), nullable=False)
    descripcion_proyecto = Column(Text, nullable=True)
    
    #LLAVES FORANEAS Y RELACIONES
    encargado_proyecto_id = Column(Integer, ForeignKey("empleados.ID_empleado"))
    encargado = db.relationship('Empleado', back_populates='proyectos')

    cliente_id = Column(Integer, ForeignKey("clientes.ID_cliente"))
    cliente = db.relationship('Cliente', back_populates='proyectos')

    requisiciones = db.relationship('Requisicion', back_populates='proyecto')
    
    factura = db.relationship('FacturaCliente', uselist=False, back_populates='proyecto')

    recibos = db.relationship('Recibo', back_populates='proyecto')

    def __init__(self, cod_proyecto, nombre_proyecto, descripcion_proyecto, cliente_id, encargado_proyecto_id): 
        self.cod_proyecto = cod_proyecto     
        self.nombre_proyecto = nombre_proyecto
        self.descripcion_proyecto = descripcion_proyecto
        self.cliente_id = cliente_id
        self.encargado_proyecto_id = encargado_proyecto_id

    def __repr__(self):
        return f'<Proyecto {self.nombre_proyecto}>'


class ProyectoSchema(ma.Schema): 
    encargado = fields.Nested(EmpleadoSchema, only=('nombre', 'apellido', 'cargo' ,'cod_empleado'))
    cliente = fields.Nested(ClienteSchema,only=('ID_cliente', 'nombre_cliente', 'apellido_cliente'))
    requisiciones = fields.List(fields.Nested('RequisicionSchema', exclude=('proyecto',)))

    class Meta():
        fields = ('nro_proyecto', 'cod_proyecto','nombre_proyecto','descripcion_proyecto', 'cliente', 'encargado', 'requisiciones')

class ProyectoRequisicionSchema(ma.Schema):
    encargado = fields.Nested(EmpleadoRequisicionSchema)
    cliente = fields.Nested(ClienteSchema, only=('nombre_cliente', 'apellido_cliente', 'telefono_cliente', 'direccion_cliente'))

    class Meta():
        fields = ('nro_proyecto', 'cod_proyecto','nombre_proyecto','descripcion_proyecto', 'cliente', 'encargado')

class ProyectoFacturaSchema(ma.Schema):
    encargado = fields.Nested(EmpleadoRequisicionSchema)
    class Meta:
        fields = ('encargado',)