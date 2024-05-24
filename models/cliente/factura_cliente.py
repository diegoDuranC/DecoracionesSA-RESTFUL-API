from app import ma,db
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric, Float
from datetime import datetime
from marshmallow import fields

from models.proyecto import ProyectoRequisicionSchema, ProyectoFacturaSchema
from models.cliente.cliente import ClienteFacturaSchema
from .detalle_factura import DetalleFacturaSchema
# from models.material.material import MaterialSchema
# from models.rrhh.empleado import EmpleadoSchema

class FacturaCliente(db.Model):
    __tablename__ = "facturas_cliente"

    nro_factura = Column(Integer, autoincrement=True, primary_key=True)
    fecha = Column(Date)
    costo_mano_obra = Column(Float, nullable=False)
    direccion_envio = Column(String(255), nullable=False)
    total = Column(Numeric(8,2), default=0)
    
    #TABLAS CONECTADAS
    '''
        PROYECTO
        CLIENTE
        CUENTA POR COBRAR
    '''
    cliente_id = Column(Integer, ForeignKey("clientes.id_cliente"))
    cliente = db.relationship('Cliente', back_populates='facturas')

    proyecto_id = Column(Integer, ForeignKey("proyectos.numero_proyecto"))
    proyecto = db.relationship('Proyecto', back_populates='factura')

    detalles = db.relationship('DetalleFactura', back_populates='factura')

    cuenta_por_cobrar = db.relationship('CuentaPorCobrar', back_populates='factura', uselist=False)

    def __init__(self, costo_mano_obra, direccion_envio, cliente_id, proyecto_id, total):
        self.fecha = datetime.now().strftime("%Y-%m-%d")
        self.costo_mano_obra = costo_mano_obra
        self.direccion_envio = direccion_envio
        self.cliente_id = cliente_id
        self.proyecto_id = proyecto_id
        self.total = total


class FacturaSchema(ma.Schema):
    cliente = fields.Nested(ClienteFacturaSchema)
    proyecto = fields.Nested(ProyectoFacturaSchema)
    detalles = fields.List(fields.Nested(DetalleFacturaSchema, exclude=("nro_factura",)))

    class Meta():
        model = FacturaCliente
        fields = ("nro_factura", "fecha", "costo_mano_obra", "direccion_envio", "total", "proyecto", "cliente", "detalles")

