from flask import Blueprint, jsonify, request
from services.facades.transaccion_inventario_facade import TransaccionInventarioFacade
from flask_cors import cross_origin

transaccion_inventario_bp = Blueprint('transaccion_inventario_bp', __name__)
transaccion_inventario_facade = TransaccionInventarioFacade()

# Obtener todas las transacciones de inventario
@cross_origin()
@transaccion_inventario_bp.route("/transacciones", methods=['GET'])
def obtener_todas_las_transacciones():
    result = transaccion_inventario_facade.obtener_todas_las_transacciones()
    return jsonify(result)

# Obtener transacciones de inventario por fecha
# Params fecha_inicio fecha_fin formato YYYY-mm-dd
@cross_origin()
@transaccion_inventario_bp.route("/transacciones/fecha", methods=['GET'])
def obtener_transacciones_por_fecha():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    result = transaccion_inventario_facade.obtener_transacciones_por_fecha(fecha_inicio, fecha_fin)
    return jsonify(result)

# Obtener transacciones de inventario por código de material
@cross_origin()
@transaccion_inventario_bp.route("/transacciones/material/<int:codigo_material>", methods=['GET'])
def obtener_transacciones_por_codigo_material(codigo_material):
    result = transaccion_inventario_facade.obtener_transacciones_por_codigo_material(codigo_material)
    return jsonify(result)

# Obtener una transacción específica por ID
@cross_origin()
@transaccion_inventario_bp.route("/transacciones/<int:id>", methods=['GET'])
def obtener_transaccion_por_id(id):
    result = transaccion_inventario_facade.obtener_transaccion_por_id(id)
    return jsonify(result)

'''
    Ruta: /transacciones/entrada/material/<int:codigo_material>
    Método: GET
    Función: obtener_transacciones_entrada_por_codigo_material
    Descripción: Esta ruta permite obtener todas las transacciones de entrada (tipo E) para un material específico identificado por su código.
'''

# Obtener transacciones de entrada por código de material
@cross_origin()
@transaccion_inventario_bp.route("/transacciones/entrada/material/<int:codigo_material>", methods=['GET'])
def obtener_transacciones_entrada_por_codigo_material(codigo_material):
    result = transaccion_inventario_facade.obtener_transacciones_entrada_por_codigo_material(codigo_material)
    return jsonify(result)

# Obtener transacciones de salida por código de material
'''
    Ruta: /transacciones/salida/material/<int:codigo_material>
    Método: GET
    Función: obtener_transacciones_salida_por_codigo_material
    Descripción: Esta ruta permite obtener todas las transacciones de salida (tipo S) para un material específico identificado por su código.
'''
@cross_origin()
@transaccion_inventario_bp.route("/transacciones/salida/material/<int:codigo_material>", methods=['GET'])
def obtener_transacciones_salida_por_codigo_material(codigo_material):
    result = transaccion_inventario_facade.obtener_transacciones_salida_por_codigo_material(codigo_material)
    return jsonify(result)

'''
Ejemplo solicitud

{
    "codigo_material": 2,
    "descripcion": "Nueva descripción",
    "precio_unitario": 15.00,
    "fecha_transaccion": "2024-05-26",
    "cantidad_entrada": 20.0,
    "cantidad_salida": 0.0,
    "existencia_salida": 200.0,
    "tipo_transaccion": "E"
}

'''
# Actualizar una transacción de inventario por su ID
@cross_origin()
@transaccion_inventario_bp.route("/transaccion_inventario/<int:id>", methods=['PUT'])
def actualizar_transaccion_inventario(id):
    data = request.get_json()
    result = transaccion_inventario_facade.actualizar_transaccion(id, data)
    return jsonify(result)