from flask_cors import cross_origin
from flask import jsonify, request, Blueprint

from services.facades.cuenta_cobrar_cliente_facade import CuentaPorCobrarClienteFacade

cuenta_cobrar_bp = Blueprint('cuenta_cobrar', __name__)

cuenta_por_cobrar_facade = CuentaPorCobrarClienteFacade()

#GENERAR LAS CUENTAS POR COBRAR
#Necesita el nro de factura (id de factura)
@cross_origin()
@cuenta_cobrar_bp.route("/cuenta_cobrar/generar_cuenta/<int:nro_factura>", methods=['POST'])
def generar_cuenta_por_cobrar(nro_factura):
    
    request_data = request.get_json(silent=True)
    result = cuenta_por_cobrar_facade.generar_cuenta_por_cobrar(request_data=request_data, nro_factura=nro_factura)
    
    return jsonify(result)

#OBTENER LAS CUENTAS DE UN CLIENTE
#Necesita el id del cliente (id de factura)
@cross_origin()
@cuenta_cobrar_bp.route("/cuenta_cobrar/<int:id_cliente>", methods=['GET'])
def obtener_estados_cliente(id_cliente):

    result = cuenta_por_cobrar_facade.get_cuentas_cliente(id_cliente=id_cliente)

    return jsonify(result)

#Obtener las cuentas de todos los clientes 
@cuenta_cobrar_bp.route("/cuentas_cobrar", methods=['GET'])
def obtener_cuentas():
    
    result = cuenta_por_cobrar_facade.get_cuentas_cobrar()

    return jsonify(result)

# OBTENER LAS CUENTAS DE UN CLIENTE, pendientes
# Necesita el CI del cliente
@cuenta_cobrar_bp.route("/cuentas_cobrar/ci_cliente", methods=['GET'])
def obtener_cuentas_ci():
    ci_cliente = request.args.get('ci_cliente')

    if not ci_cliente:
        return jsonify({"Error": "El parámetro ci_cliente es requerido"}), 400

    result = cuenta_por_cobrar_facade.get_cuentas_cobrar_ci_pendientes(ci_cliente=ci_cliente)
    
    return jsonify(result)

#GENERAR ESTADO DE CUENTA
#NUMERO DE CUENTA
@cuenta_cobrar_bp.route("/cuentas_cobrar/estado_cuenta/<int:nro_cuenta>", methods=['GET'])
def estado_cuenta(nro_cuenta):
    estado = cuenta_por_cobrar_facade.generar_estado_cuenta(nro_cuenta)
    return jsonify(estado)