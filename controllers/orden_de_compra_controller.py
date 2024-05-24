from flask import request
from app import db
from models.compras.orden_de_compra import OrdenDeCompra
from models.compras.orden_de_compra import Deta

class OrdenCompraController():

    def create_orden(self):
        request_data = request.get_json()

        orden = OrdenDeCompra(**request_data)

        db.session.add(orden)
        db.session.commit()

        return orden

def DetalleOrden():

    def create_detalle(self):
        return 