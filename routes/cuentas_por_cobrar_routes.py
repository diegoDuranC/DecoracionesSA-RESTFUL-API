from flask_cors import cross_origin
from flask import jsonify, request, Blueprint

from services.facades.cuenta_cobrar_cliente_facade import CuentaPorCobrarClienteFacade

cuenta_cobrar_bp = Blueprint('cuenta_cobrar', __name__)

cuenta_por_cobrar_facade = CuentaPorCobrarClienteFacade()

#GENERAR LAS CUENTAS POR COBRAR
#Necesita el nro de factura (id de factura)
#SE ENVIA UN SILENT CUANDO EL CLIENTE VA A PAGAR CON EFECTIVO, ES DECIR, UN ÚNICO PAGO
"""
    Ejemplo del body para hacer un plan de pago mensual

    {
        "vencimiento": "2024-12-31",  # Fecha de vencimiento del plan de pagos
        "intervalo_pago_dias": 30      # Intervalo de pago en días (mensual)
    }

    Si no se envía un json, quiere decir que se pagará ese mismo momento, al contado y la fecha de la cuenta tomará la fecha de la factura
"""
@cuenta_cobrar_bp.route("/cuenta_cobrar/generar_cuenta/<int:nro_factura>", methods=['POST'])
def generar_cuenta_por_cobrar(nro_factura):
    
    request_data = request.get_json(silent=True)
    result = cuenta_por_cobrar_facade.generar_cuenta_por_cobrar(request_data=request_data, nro_factura=nro_factura)
    
    return jsonify(result)

#OBTENER LAS CUENTAS DE UN CLIENTE
#Necesita el id del cliente (id de factura)
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

#ELIMINAR LA CUENTA Y SUS PAGOS
@cuenta_cobrar_bp.route("/cuenta_cobrar/<int:nro_cuenta>", methods=['DELETE'])
def eliminar_cuenta(nro_cuenta):
    cuenta = cuenta_por_cobrar_facade.eliminar_cuenta_pagos(nro_cuenta)
    return jsonify(cuenta)