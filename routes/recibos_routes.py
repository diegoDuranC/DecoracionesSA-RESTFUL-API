from flask_cors import cross_origin
from flask import jsonify, request, Blueprint

from services.facades.recibo_facade import ReciboFacade

recibo_bp = Blueprint('recibo', __name__)
recibo_facade = ReciboFacade()

#################
#### RECIBOS ####
#################

#RUTA DE PRUEBA

@recibo_bp.route("/recibos", methods=['GET'])
def obtener_todos_recibos():
    result = recibo_facade.obtener_recibos()
    return jsonify(result)

#GENERA UN RECIBO
#NECESITA
'''
                Crea un recibo en base al siguiente json
            {
                "nro_cuenta" : int() -> nro_cuenta a la cual se le hara el recibo,
                "monto" : float(), decimal() -> monto a pagar,
            }
'''

@recibo_bp.route("/recibo/generar_recibo", methods=['POST'])
def generar_recibo():
    
    request_data = request.get_json()
    result = recibo_facade.crear_recibo(request_data=request_data)
    return jsonify(result)


@recibo_bp.route('/recibo/filtrar_fecha', methods=['GET'])
def recibos_por_fecha():
    # Obtiene los recibos por fecha con Query Params del argm
    # fecha_inicio = "YYYY-mm-dd"
    # fecha_fin = "YYYY-mm-dd"
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    recibos = recibo_facade.obtener_recibos_por_fecha(fecha_inicio, fecha_fin)

    return jsonify(recibos)

#DEVUELVE LOS RECIBOS FILTRADOS POR CI

@recibo_bp.route("/recibos/ci", methods=['GET'])
def recibos_ci_cliente():

    ci_cliente = request.args.get('ci_cliente')
    recibos = recibo_facade.obtener_recibos_ci_cliente(ci_cliente=ci_cliente)

    return jsonify(recibos)

#DEVUELVE LOS RECIBOS DEL DIA

@recibo_bp.route("/recibos/del_dia", methods=['GET'])
def recibos_del_dia():

    recibos = recibo_facade.obtener_recibos_del_dia()

    return jsonify(recibos)

#DEVUELVE LOS RECIBOS EN INTERVALO DE FECHA SIN DEPOSITO

@recibo_bp.route("/recibos/sin_depositar/fecha", methods=['GET'])
def recibos_del_dia_sin_depositar():

    """
    Ruta para obtener los recibos que no están asociados a un depósito en un intervalo de fechas.
    
    Parámetros de URL:
    - fecha_inicio: Fecha de inicio del intervalo (YYYY-MM-DD).
    - fecha_fin: Fecha de fin del intervalo (YYYY-MM-DD).
    
    Retorna:
    - Un diccionario con los recibos y el monto total de esos recibos.
    """
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    if not fecha_inicio or not fecha_fin:
        return jsonify({"Error": "Los parámetros fecha_inicio y fecha_fin son requeridos"}), 400

    recibos = recibo_facade.obtener_recibos_sin_deposito_monto_total(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)

    return jsonify(recibos)
