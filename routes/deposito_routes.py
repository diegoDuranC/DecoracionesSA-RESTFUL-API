from unittest import result
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from services.facades.deposito_facade import DepositoFacade

deposito_bp = Blueprint('deposito_bp', __name__)
deposito_facade = DepositoFacade()

@deposito_bp.route('/deposito', methods=['GET'])
def inicio():
    return "Testing Route"

#Obten todos los depositos
@deposito_bp.route('/depositos', methods=['GET'])
def get_depositos():
    result = deposito_facade.get_depositos()
    return jsonify(result)

#DEBE SER UN EMPLEADO DEL AREA DE VENTAS, AYUDANTE DE VENTAS

@deposito_bp.route('/deposito', methods=['POST'])
def crear_deposito():
    data = request.get_json()
    cuenta = data.get('cuenta')
    fecha = data.get('fecha')
    monto = data.get('monto')
    banco_id = data.get('banco_id')
    forma_pago = data.get('forma_pago')
    
    result = deposito_facade.crear_deposito(cuenta, fecha, monto, banco_id, forma_pago)
    return jsonify(result)


# @deposito_bp.route('/deposito/crear_desde_recibos_del_dia', methods=['POST'])
# def crear_deposito_desde_recibos_del_dia():
#     data = request.get_json()
#     cuenta = data.get('cuenta')
#     banco_id = data.get('banco_id')
#     forma_pago = data.get('forma_pago')
    
#     result = deposito_facade.crear_deposito_con_recibos_del_dia(cuenta, banco_id, forma_pago)
#     return jsonify(result)


@deposito_bp.route('/deposito/lista_recibos', methods=['POST'])
def crear_deposito_lista_recibos():
    data = request.get_json()

    recibos = data.get('recibos', [])
    cuenta = data.get('cuenta')
    banco_id = data.get('banco_id')
    forma_pago = data.get('forma_pago')

    result = deposito_facade.crear_deposito_recibos(recibos=recibos, cuenta=cuenta, banco_id=banco_id, forma_pago=forma_pago)
    return jsonify(result)