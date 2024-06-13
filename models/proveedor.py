from app import db, ma

class Proveedor(db.Model):
    __tablename__ = "proveedores"

    id_proveedor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_proveedor = db.Column(db.String(20), nullable=False)
    nombre = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(8), nullable=False)
    empresa = db.Column(db.String(60), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)

    facturas = db.relationship('FacturaOrdenCompra', back_populates='proveedor')

    def __init__(self, nombre, telefono, empresa, direccion, cod_proveedor):
        self.nombre = nombre
        self.telefono = telefono
        self.empresa = empresa
        self.direccion = direccion
        self.cod_proveedor = cod_proveedor

        return f'Proveedor {self.nombre} de la empresa {self.empresa}'

class ProveedorSchema(ma.Schema):
    class Meta:
        fields = ('id_proveedor', 'cod_proveedor', 'nombre', 'telefono', 'empresa', 'direccion')