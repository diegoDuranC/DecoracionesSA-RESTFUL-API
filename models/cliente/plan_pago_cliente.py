from app import db,ma
from sqlalchemy import Column, Integer, Date, Numeric, ForeignKey

class PlanPagoCliente(db.Model):

    __tablename__ = 'plan_pagos_cliente'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date)
    monto = Column(Numeric(8,2))
    nro_cuenta = Column(Integer, ForeignKey("cuentas_por_cobrar.nro_cuenta"))

    #Relacion
    cuenta = db.relationship('CuentaPorCobrar', back_populates='pagos')

    def __init__(self, fecha, monto, nro_cuenta):
        self.fecha = fecha
        self.monto = monto
        self.nro_cuenta = nro_cuenta

class PlanPagoClienteSchema(ma.Schema):
    class Meta():
        fields = ("fecha", "monto")