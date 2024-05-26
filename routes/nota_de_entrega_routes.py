from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from services.facades.nota_de_entrega_facade import NotaDeEntregaFacade

nota_entrega_bp = Blueprint('nota_entrega_bp', __name__)
nota_de_entrega_facade = NotaDeEntregaFacade()

# Ruta para agregar una nueva nota de entrega
# Parámetros JSON:
# {
#   "nro_orden": 1,
#   "materiales_recibidos": [
#       {"cod_material": 1, "cantidad_recibida": 5},
#       {"cod_material": 2, "cantidad_recibida": 3}
#   ]
# }
@cross_origin()
@nota_entrega_bp.route('/nota_de_entrega', methods=['POST'])
def agregar_nota_de_entrega():
    data = request.get_json()
    nro_orden = data.get('nro_orden')
    materiales_recibidos = data.get('materiales_recibidos')
    result = nota_de_entrega_facade.agregar_nota_de_entrega(nro_orden, materiales_recibidos)
    return jsonify(result)

# Ruta para obtener una nota de entrega específica por su número de nota
# Parámetros de URL:
# - nro_nota: Número de la nota de entrega
@cross_origin()
@nota_entrega_bp.route('/nota_de_entrega/<int:nro_nota>', methods=['GET'])
def obtener_nota_de_entrega(nro_nota):
    result = nota_de_entrega_facade.obtener_nota_de_entrega(nro_nota)
    return jsonify(result)

# Ruta para obtener todas las notas de entrega
@cross_origin()
@nota_entrega_bp.route('/notas_de_entrega', methods=['GET'])
def obtener_notas_de_entrega():
    result = nota_de_entrega_facade.obtener_todas_las_notas_de_entrega()
    return jsonify(result)

# Ruta para obtener entregas pendientes específicas por su número de nota
# Parámetros de URL:
# - nro_nota: Número de la nota de entrega
@cross_origin()
@nota_entrega_bp.route('/entrega_pendiente/<int:nro_nota>', methods=['GET'])
def obtener_entrega_pendiente(nro_nota):
    result = nota_de_entrega_facade.obtener_entrega_pendiente_nro_nota(nro_nota)
    return jsonify(result)

# Ruta para actualizar el estado de una entrega pendiente
# Parámetros de URL:
# - id: ID de la entrega pendiente
# Parámetros JSON:
# {
#   "estado": "ENTREGADO"
# }
# @cross_origin()
# @nota_entrega_bp.route('/entrega_pendiente/<int:id>', methods=['PUT'])
# def actualizar_estado_entrega_pendiente(id):
#     data = request.get_json()
#     estado = data.get('estado')
#     result = nota_de_entrega_facade.actualizar_entrega_pendiente(id, estado)
#     return jsonify(result)
