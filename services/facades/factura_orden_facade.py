from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app import db
from models.compras.factura_orden import FacturaOrdenCompra, FacturaOrdenCompraSchema
from models.compras.orden_de_compra import OrdenDeCompra
from models.proveedor import Proveedor
from models.banco.deposito import Deposito

class FacturaOrdenCompraFacade:
    def __init__(self):
        self.factura_schema = FacturaOrdenCompraSchema()
        self.factura_schemas = FacturaOrdenCompraSchema(many=True)

    def crear_factura(self, nro_orden, nro_proveedor, monto, descripcion, nro_deposito):
        try:
            nueva_factura = FacturaOrdenCompra(
                nro_orden=nro_orden,
                nro_proveedor=nro_proveedor,
                monto=monto,
                fecha=datetime.now().strftime("%Y-%m-%d"),
                descripcion=descripcion,
                nro_deposito=nro_deposito
            )
            db.session.add(nueva_factura)
            db.session.commit()
            return self.factura_schema.dump(nueva_factura)
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"Error": str(e)}

    def obtener_factura(self, nro_factura):
        factura = FacturaOrdenCompra.query.get(nro_factura)
        if not factura:
            return {"Error": "Factura no encontrada"}
        return self.factura_schema.dump(factura)

    def obtener_todas_las_facturas(self):
        facturas = FacturaOrdenCompra.query.all()
        return self.factura_schemas.dump(facturas)
