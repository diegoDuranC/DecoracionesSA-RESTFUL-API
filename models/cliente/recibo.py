from datetime import datetime
from app import db, ma
from sqlalchemy import Integer, Numeric, String, Date, ForeignKey, Column
from marshmallow import fields

from models.cliente.cuenta_cobrar import CuentaPorCobrarRecibo
from models.rrhh.empleado import EmpleadoSchema
from models.proyecto import ProyectoSchema

class Recibo(db.Model):
    __tablename__ = "recibos"

    nro_recibo = Column(Integer, autoincrement=True, primary_key=True)
    fecha = Column(Date)
    ci_cliente = Column(String, nullable=False)
    monto = Column(Numeric(8,2))

    # Relación muchos a uno con CuentaPorCobrar
    cuenta_por_cobrar_id = Column(Integer, ForeignKey('cuentas_por_cobrar.nro_cuenta'))
    cuenta_por_cobrar = db.relationship('CuentaPorCobrar', back_populates='recibos')

    # Relación muchos a uno con Empleado
    empleado_id = Column(Integer, ForeignKey('empleados.ID_empleado'))
    empleado = db.relationship('Empleado', back_populates='recibos')

    # Relación uno a uno con Deposito
    deposito_id = Column(Integer, ForeignKey('depositos.nro_deposito'), nullable=True)
    deposito = db.relationship('Deposito', back_populates='recibo')

    # Relacion muchos a uno con Proyecto
    numero_proyecto = Column(Integer, ForeignKey('proyectos.nro_proyecto'))
    proyecto = db.relationship('Proyecto', back_populates='recibos')

    def __init__(self, ci_cliente, monto, cuenta_por_cobrar_id, empleado_id, deposito_id, numero_proyecto):
        self.ci_cliente = ci_cliente
        self.fecha = datetime.now().strftime("%Y-%m-%d")
        self.monto = monto
        self.cuenta_por_cobrar_id = cuenta_por_cobrar_id
        self.empleado_id = empleado_id
        self.deposito_id = deposito_id
        self.numero_proyecto = numero_proyecto

class ReciboSchema(ma.Schema):
    empleado = fields.Nested(EmpleadoSchema, only=('nombre_empleado', 'apellido_empleado', 'codigo_empleado'))
    proyecto = fields.Nested(ProyectoSchema, only=('numero_proyecto',))
    cuenta_por_cobrar = fields.Nested(CuentaPorCobrarRecibo, only=('nro_cuenta',))
    class Meta():
        fields = ("nro_recibo", "fecha", "ci_cliente", "monto", "empleado", "proyecto", "cuenta_por_cobrar", 'deposito_id')