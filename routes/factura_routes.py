from .cliente_routes import cliente_bp

from flask_cors import cross_origin
from flask import jsonify, request, Blueprint

from models.proyecto import Proyecto
from services.facades.factura_cliente_facade import FacturaClienteFacade


factura_cliente_bp = Blueprint('factura_cliente', __name__)

factura_facade = FacturaClienteFacade()

#CREAR LA FACTURA CLIENTE
#SE NECESITA EL NUMERO DE PROYECTO PARA GENERAR LA FACTURA
@factura_cliente_bp.route("/factura_cliente/crear_factura/<int:nro_proyecto>", methods=['GET'])
def crear_factura(nro_proyecto):
    factura = factura_facade.crear_factura(nro_proyecto)

    return jsonify(factura)

#OBTENER FACTURAS
@factura_cliente_bp.route("/facturas_cliente", methods=['GET'])
def obtener_factura():
    facturas = factura_facade.get_facturas()

    return jsonify(facturas)

#OBTENER FACTURAS POR CLIENTE
@factura_cliente_bp.route("/factura_cliente/cliente/<int:id_cliente>", methods=['GET'])
def obtener_factura_cliente_id(id_cliente):
    facturas = factura_facade.get_facturas_cliente_id(id_cliente)

    return jsonify(facturas)

#OBTENER FACTURAS POR CI DEL CLIENTE
@factura_cliente_bp.route("/factura_cliente/cliente/ci", methods=['GET'])
def obtener_factura_cliente_ci():
    ci = request.args.get('ci')
    facturas = factura_facade.get_facturas_cliente_ci(ci)

    return jsonify(facturas)

@factura_cliente_bp.route("/factura_cliente/<int:nro_factura>", methods=['DELETE'])
def eliminar_factura(nro_factura):
    factura = factura_facade.eliminar_factura(nro_factura)

    return jsonify(factura)