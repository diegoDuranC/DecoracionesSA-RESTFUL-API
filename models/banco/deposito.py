from app import ma, db
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric

class Deposito(db.Model):
    
    __tablename__ = 'depositos'

    nro_deposito = Column(Integer, primary_key=True, autoincrement=True)
    cuenta = Column(String(15), nullable=False)
    fecha = Column(Date)
    monto = Column(Numeric(8,2))

    banco_id = Column(Integer, ForeignKey("bancos.id_banco"))
    banco = db.relationship('Banco', back_populates='depositos')

    empleado_id = Column(Integer, ForeignKey("empleados.codigo_empleado"))
    empleado = db.relationship('Empleado', back_populates='depositos')

    # Relación uno a uno con Recibo
    recibo = db.relationship('Recibo', uselist=False, back_populates='deposito')

    # Relación uno a uno con FacturaOrdenCompra
    factura_orden_compra = db.relationship('FacturaOrdenCompra', uselist=False, back_populates='deposito')

    def __init__(self, cuenta, fecha, monto, banco_id):
        self.cuenta = cuenta
        self.fecha = fecha
        self.monto = monto
        self.banco_id = banco_id

class DepositoSchema(ma.Schema):
    class Meta():
        fields = ("nro_deposito", "cuenta", "monto", "fecha", "banco_id")
