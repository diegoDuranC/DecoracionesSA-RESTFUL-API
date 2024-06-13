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
@nota_entrega_bp.route('/nota_de_entrega/<int:nro_nota>', methods=['GET'])
def obtener_nota_de_entrega(nro_nota):
    result = nota_de_entrega_facade.obtener_nota_de_entrega(nro_nota)
    return jsonify(result)

# Ruta para obtener todas las notas de entrega
@nota_entrega_bp.route('/notas_de_entrega', methods=['GET'])
def obtener_notas_de_entrega():
    result = nota_de_entrega_facade.obtener_todas_las_notas_de_entrega()
    return jsonify(result)

#RUTA PARA ELIMINAR UNA NOTA DE ENTREGA, CON LAS TRANSACCIONES, Y AJUSTE DE LAS EXISTENCIAS DE MATERIAL
@nota_entrega_bp.route('/nota_de_entrega/<int:nro_nota>', methods=['DELETE'])
def eliminar_nota_de_entrega(nro_nota):
    resultado = nota_de_entrega_facade.eliminar_nota_de_entrega(nro_nota)
    return jsonify(resultado)