from .cliente_routes import cliente_bp
from flask_cors import cross_origin
from flask import jsonify, request

from services.facades.recibo_facade import ReciboFacade
recibo_facade = ReciboFacade()

#################
#### RECIBOS ####
#################

#GENERAR EL RECIBO CON UN JSON CON LOS PARÁMETROS:

# {
#     "nro_cuenta" : int() -> nro_cuenta a la cual se le hara el recibo,
#     "monto" : float(), decimal() -> monto a pagar,
# }

@cross_origin()
@cliente_bp.route("/cliente/recibo/generar_recibo", methods=['POST'])
def generar_recibo():
    
    request_data = request.get_json()
    result = recibo_facade.crear_recibo(request_data=request_data)
    return jsonify(result)

#DEVUELVE LOS RECIBOS POR INTERVALO DE FECHAS
#Query Params
#fecha_inicio
#fecha_fin

@cross_origin()
@cliente_bp.route('/cliente/recibo/filtrar_fecha', methods=['GET'])
def recibos_por_fecha():

    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    recibos = recibo_facade.obtener_recibos_por_fecha(fecha_inicio, fecha_fin)

    return jsonify(recibos)

#DEVUELVE LOS RECIBOS FILTRADOS POR CI
@cross_origin()
@cliente_bp.route("/cliente/ci/recibos", methods=['GET'])
def recibos_ci_cliente():

    ci_cliente = request.args.get('ci_cliente')
    recibos = recibo_facade.obtener_recibos_ci_cliente(ci_cliente=ci_cliente)

    return jsonify(recibos)

#DEVUELVE LOS RECIBOS DEL DIA
@cross_origin()
@cliente_bp.route("/cliente/recibos/del_dia", methods=['GET'])
def recibos_del_dia():

    recibos = recibo_facade.obtener_recibos_del_dia()

    return jsonify(recibos)
