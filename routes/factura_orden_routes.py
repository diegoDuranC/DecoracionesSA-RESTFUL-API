from flask import Blueprint, request, jsonify
from services.facades.factura_orden_facade import FacturaOrdenCompraFacade

factura_orden_bp = Blueprint('factura_orden_bp', __name__)
factura_orden_facade = FacturaOrdenCompraFacade()

# Ruta para crear una nueva factura de orden de compra
@factura_orden_bp.route('/factura_orden', methods=['POST'])
def crear_factura_orden():
    data = request.get_json()
    nro_orden = data.get('nro_orden')
    nro_proveedor = data.get('nro_proveedor')
    monto = data.get('monto')
    descripcion = data.get('descripcion')
    nro_deposito = data.get('nro_deposito')
    result = factura_orden_facade.crear_factura(nro_orden, nro_proveedor, monto, descripcion, nro_deposito)
    return jsonify(result)

# Ruta para obtener una factura específica por su número de factura
@factura_orden_bp.route('/factura_orden/<int:nro_factura>', methods=['GET'])
def obtener_factura_orden(nro_factura):
    result = factura_orden_facade.obtener_factura(nro_factura)
    return jsonify(result)

# Ruta para obtener todas las facturas de órdenes de compra
@factura_orden_bp.route('/facturas_ordenes', methods=['GET'])
def obtener_todas_las_facturas_ordenes():
    result = factura_orden_facade.obtener_todas_las_facturas()
    return jsonify(result)
