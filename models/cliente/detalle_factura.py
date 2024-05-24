from app import ma, db
from sqlalchemy import Column, Integer, ForeignKey, Float, String, Numeric

class DetalleFactura(db.Model):
    __tablename__ = 'detalle_factura'

    id = Column(Integer, autoincrement=True, primary_key=True)
    nro_factura = Column(Integer, ForeignKey("facturas_cliente.nro_factura"))
    cod_material = Column(Integer, ForeignKey("materiales.codigo_material"))
    nombre_material = Column(String(255))
    precio_unitario = Column(Float)
    cantidad = Column(Float)
    sub_total = Column(Numeric)

    factura = db.relationship('FacturaCliente', back_populates = 'detalles')

    def __init__(self, cod_material, nombre_material, precio_unitario, cantidad, sub_total, nro_factura):
        self.nro_factura = nro_factura
        self.cod_material = cod_material
        self.nombre_material = nombre_material
        self.precio_unitario = precio_unitario
        self.cantidad = cantidad
        self.sub_total = sub_total

class DetalleFacturaSchema(ma.Schema):
    class Meta():
        model = DetalleFactura
        fields = ("nro_factura", "cod_material", "nombre_material", "cantidad", "precio_unitario", "sub_total")
        include_fk = True

# class DetalleFacturaSchemas(ma.Schema):
#     class Meta():