from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from services.facades.orden_de_compra_facade import OrdenDeCompraFacade

orden_compra_bp = Blueprint("orden_compra", __name__)
fachada_orden_compra = OrdenDeCompraFacade()

#CREAR ORDEN DE COMPRA
#FORMATO DE JSON
'''
    {
        "descripcion" : "Compra de materiales para proyecto X",
        "materiales" : [
            {"codigo_material" : 1, "cantidad_requerida": 5, "precio_material": 40},
            {"codigo_material" : 2, "cantidad_requerida" : 10, "precio_material": 20}
        ]
    }
'''
@cross_origin
@orden_compra_bp.route('/ordenes_de_compra', methods=['POST'])
def crear_orden_de_compra():

    data = request.json
    descripcion = data.get('descripcion')
    materiales = data.get('materiales')
       
    resultado = fachada_orden_compra.crear_orden_de_compra(descripcion, materiales)
    return jsonify(resultado)

#OBTENER ORDEN POR ID
@cross_origin()
@orden_compra_bp.route('/ordenes_de_compra/<int:nro_orden>', methods=['GET'])
def obtener_orden_por_id(nro_orden):

    resultado = fachada_orden_compra.obtener_orden_por_id(nro_orden)
    return jsonify(resultado)

#OBTEN TODAS LAS ORDENDES DE COMPRA
@cross_origin()
@orden_compra_bp.route('/ordenes_de_compra', methods=['GET'])
def obtener_todas_las_ordenes():

    resultado = fachada_orden_compra.obtener_todas_las_ordenes()
    return jsonify(resultado)

#FALTA VERIFICAR LA LÓGICA SI, EL PROVEEDOR NO ENTREGA TODOS LOS MATERIALES Y SE ALMACENAN SOLO LOS RECIBIDOS
#GUARDANDO UN REGISTRO DE PEDIDOS EN ESPERA O REZAGADOS QUE DESCRIBA QUE MATERIAL FALTA, CUANTO Y DE QUE ORDEN
@cross_origin()
@orden_compra_bp.route('/ordenes_de_compra/<int:nro_orden>/nota_de_entrega', methods=['POST'])
def agregar_nota_de_entrega(nro_orden):
    data = request.json
    fecha = data.get('fecha')
    
    resultado = fachada_orden_compra.agregar_nota_de_entrega(nro_orden, fecha)
    return jsonify(resultado)