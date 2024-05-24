from .cliente_routes import cliente_bp

from flask_cors import cross_origin
from flask import jsonify, request

from services.facades.cuenta_cobrar_cliente_facade import CuentaPorCobrarClienteFacade

cuenta_por_cobrar_facade = CuentaPorCobrarClienteFacade()

#GENERAR LAS CUENTAS POR COBRAR
#Necesita el nro de factura (id de factura)
@cross_origin()
@cliente_bp.route("/cliente/cuenta_cobrar/generar_cuenta/<int:nro_factura>", methods=['POST'])
def generar_cuenta_por_cobrar(nro_factura):
    
    request_data = request.get_json(silent=True)
    result = cuenta_por_cobrar_facade.generar_cuenta_por_cobrar(request_data=request_data, nro_factura=nro_factura)
    
    return jsonify(result)

#OBTENER LAS CUENTAS DE UN CLIENTE
#Necesita el id del cliente (id de factura)
@cross_origin()
@cliente_bp.route("/cliente/cuenta_cobrar/<int:id_cliente>", methods=['GET'])
def obtener_estados_cliente(id_cliente):

    result = cuenta_por_cobrar_facade.get_cuentas_cliente(id_cliente=id_cliente)

    return jsonify(result)
