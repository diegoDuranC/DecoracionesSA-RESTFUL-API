from app import db, ma

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ci_cliente = db.Column(db.String(7), nullable=False, unique=True)
    nombre_cliente = db.Column(db.String(80), nullable=False)
    apellido_cliente = db.Column(db.String(80), nullable=False)
    direccion_cliente = db.Column(db.String(255), nullable=False)
    telefono_cliente = db.Column(db.String(8), nullable=False)

    def __init__(self, ci_cliente, nombre_cliente, apellido_cliente, direccion_cliente, telefono_cliente):
        self.ci_cliente = ci_cliente
        self.nombre_cliente = nombre_cliente
        self.apellido_cliente = apellido_cliente
        self.direccion_cliente = direccion_cliente
        self.telefono_cliente = telefono_cliente

    def __repr__ (self):
        return '<Cliente %r>' % self.nombre_cliente % self.apellido_cliente % 'CI' % self.ci_cliente

class ClienteSchema(ma.Schema):
    class Meta:
        fields = ('id_cliente', 'ci_cliente', 'nombre_cliente', 'apellido_cliente', 'direccion_cliente', 'telefono_cliente')
