from app import db, ma

class Cliente(db.Model):
    __tablename__ = 'clientes'

    ID_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_cliente = db.Column(db.String(20), nullable=False, unique=True)
    ci_cliente = db.Column(db.String(7), nullable=False, unique=True)
    nombre_cliente = db.Column(db.String(80), nullable=False)
    apellido_cliente = db.Column(db.String(80), nullable=False)
    direccion_cliente = db.Column(db.String(255), nullable=False)
    telefono_cliente = db.Column(db.String(8), nullable=False)

    proyectos = db.relationship('Proyecto', back_populates='cliente')
    facturas = db.relationship('FacturaCliente', back_populates='cliente')
    cuentas_por_cobrar = db.relationship('CuentaPorCobrar', back_populates='cliente')
    recibos = db.relationship('Recibo', back_populates='cliente')

    def __init__(self, cod_cliente, ci_cliente, nombre_cliente, apellido_cliente, direccion_cliente, telefono_cliente):
        self.cod_cliente = cod_cliente
        self.ci_cliente = ci_cliente
        self.nombre_cliente = nombre_cliente
        self.apellido_cliente = apellido_cliente
        self.direccion_cliente = direccion_cliente
        self.telefono_cliente = telefono_cliente

    def __repr__ (self):
        return '<Cliente nombre=%r apellido=%r CI=%r>' % (self.nombre_cliente, self.apellido_cliente, self.ci_cliente)

class ClienteSchema(ma.Schema):
    class Meta:
        fields = ('ID_cliente', 'cod_cliente', 'ci_cliente', 'nombre_cliente', 'apellido_cliente', 'direccion_cliente', 'telefono_cliente')

class ClienteFacturaSchema(ma.Schema):
    class Meta:
        fields = ('nombre_cliente', 'apellido_cliente', 'numero_cliente', 'ci_cliente')