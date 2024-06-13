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

    #OBTIENE EL MONTO EN BASE AL MONTO DEL DEPOSITO, ES DECIR, COMO SI SE PAGARA DE UNA SOLA VEZ todo su importe
    def crear_factura(self, nro_orden, id_proveedor, descripcion, nro_deposito):
        try:
            deposito = Deposito.query.get(nro_deposito)

            if not deposito: 
                return {"error" : "deposito no encontrado"}
            
            nueva_factura = FacturaOrdenCompra(
                nro_orden=nro_orden,
                id_proveedor=id_proveedor,
                monto=deposito.monto,
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
    
    def actualizar_factura(self, nro_factura, monto, fecha, descripcion, nro_deposito, nro_orden):

        deposito = Deposito.query.get(nro_deposito)

        if not deposito:
            return {"mensaje" : "Deposito no encontrado"}
        
        factura = FacturaOrdenCompra.query.get(nro_factura)

        if not monto:
            monto = deposito.monto

        if factura:
            factura.monto = monto
            factura.fecha = fecha
            factura.descripcion = descripcion
            factura.nro_deposito = nro_deposito
            db.session.commit()

            return FacturaOrdenCompraSchema().dump(factura)
        
        return {'mensaje': 'Factura no encontrada'}, 404

    def eliminar_factura(self, nro_factura):
        factura = FacturaOrdenCompra.query.get(nro_factura)
        if factura:
            db.session.delete(factura)
            db.session.commit()
            return {'mensaje': 'Factura eliminada exitosamente'}
        return {'mensaje': 'Factura no encontrada'}, 404
