from flask import Blueprint, jsonify, request
from services.facades.orden_de_compra_facade import OrdenDeCompraFacade, EstadoCompra

orden_compra_bp = Blueprint("orden_compra", __name__)
fachada_orden_compra = OrdenDeCompraFacade()

#CREAR ORDEN DE COMPRA
#FORMATO DE JSON
'''
    {
        "descripcion" : "Compra de materiales para proyecto X",
        "cod_orden" : "COMPMAT-10289"
        "materiales" : [
            {"ID_material" : 1, "cantidad_requerida": 5, "precio_material": 40},
            {"ID_material" : 2, "cantidad_requerida" : 10, "precio_material": 20}
        ]
    }
'''

@orden_compra_bp.route('/orden_de_compra', methods=['POST'])
def crear_orden_de_compra():

    data = request.json
    descripcion = data.get('descripcion')
    materiales = data.get('materiales')
    cod_orden = data.get('cod_orden')
       
    resultado = fachada_orden_compra.crear_orden_de_compra(
        descripcion=descripcion, 
        materiales=materiales, 
        cod_orden=cod_orden
    )
    
    return jsonify(resultado)

#OBTENER ORDEN POR ID

@orden_compra_bp.route('/orden_de_compra/<int:nro_orden>', methods=['GET'])
def obtener_orden_por_id(nro_orden):

    resultado = fachada_orden_compra.obtener_orden_por_id(nro_orden)
    return jsonify(resultado)

#OBTEN TODAS LAS ORDENDES DE COMPRA

@orden_compra_bp.route('/ordenes_de_compra', methods=['GET'])
def obtener_todas_las_ordenes():

    resultado = fachada_orden_compra.obtener_todas_las_ordenes()
    return jsonify(resultado)

#OBTENER LAS ORDENES PENDIENTES
@orden_compra_bp.route('/ordenes_de_compra/pendientes', methods=['GET'])
def obtener_ordenes_pendientes():

    resultado = fachada_orden_compra.obtener_ordenes_pendientes()
    return jsonify(resultado)

#OBTENER LAS ORDENES PARCIALMENTE-SATIFECHAS
@orden_compra_bp.route('/ordenes_de_compra/parcialmente_satisfechas', methods=['GET'])
def obtener_ordenes_parcialmente_satisfechas():

    resultado = fachada_orden_compra.obtener_ordenes_parcialmente_satisfechas()
    return jsonify(resultado)

#OBTENER LAS ORDENES SATISFECHAS
@orden_compra_bp.route('/ordenes_de_compra/satisfechas', methods=['GET'])
def obtener_ordenes_satisfechas():

    resultado = fachada_orden_compra.obtener_ordenes_satisfechas()
    return jsonify(resultado)

#RUTA QUE DEVUELVE UNA LISTA 
#CON TODOS LOS ESTADOS POSIBLES PARA LA ORDEN DE COMPRA
@orden_compra_bp.route('/estados_compra', methods=['GET'])
def obtener_estados_compra():
    estados = [estado.name for estado in EstadoCompra]

    return jsonify(estados)

#RUTA PARA ACTUALIZAR EL ENCABEZADO DE LA ORDEN DE COMPRA
'''
    {
        "cod_orden": "CODACT",
        "descripcion": "Orden de prueba Actualizada"
    }
'''
@orden_compra_bp.route('/orden_de_compra/<int:nro_orden>', methods=['PUT'])
def actualizar_orden_de_compra(nro_orden):
    data = request.json
    descripcion = data.get('descripcion')
    cod_orden = data.get('cod_orden')
    estado_compra = data.get('estado_compra')

    resultado = fachada_orden_compra.actualizar_orden_de_compra(
        nro_orden=nro_orden, 
        descripcion=descripcion, 
        cod_orden=cod_orden, 
        estado_compra=estado_compra
    )
    
    return jsonify(resultado)

#RUTA PARA ACTUALIZAR EL DETALLE DE LA ORDEN
'''
    EJEMPLO RUTA: /detalle_orden_de_compra/2

    {
        "cantidad_requerida": 5,
        "precio_material": 10
    }
'''
@orden_compra_bp.route('/detalle_orden_de_compra/<int:id_detalle>', methods=['PUT'])
def actualizar_detalle_orden_de_compra(id_detalle):
    data = request.json
    cantidad_requerida = data.get('cantidad_requerida')
    precio_material = data.get('precio_material')
    
    resultado = fachada_orden_compra.actualizar_detalle_orden_de_compra(
        id_detalle=id_detalle, 
        cantidad_requerida=cantidad_requerida, 
        precio_material=precio_material
    )
    
    return jsonify(resultado)

#RTUA PARA ELIMINAR LA ORDEN Y SUS DETALLES
@orden_compra_bp.route('/orden_de_compra/<int:nro_orden>', methods=['DELETE'])
def eliminar_orden_de_compra(nro_orden):
    resultado = fachada_orden_compra.eliminar_orden_de_compra(nro_orden)
    return jsonify(resultado)

#RUTA PARA ELIMINAR UN ELEMENTO DE DETALLES
@orden_compra_bp.route('/detalle_orden_de_compra/<int:id_detalle>', methods=['DELETE'])
def eliminar_detalle_orden(id_detalle):
    resultado = fachada_orden_compra.eliminar_detalle_orden(id_detalle)
    return jsonify(resultado)

#FALTA VERIFICAR LA LÓGICA SI, EL PROVEEDOR NO ENTREGA TODOS LOS MATERIALES Y SE ALMACENAN SOLO LOS RECIBIDOS
#GUARDANDO UN REGISTRO DE PEDIDOS EN ESPERA O REZAGADOS QUE DESCRIBA QUE MATERIAL FALTA, CUANTO Y DE QUE ORDEN

# @orden_compra_bp.route('/ordenes_de_compra/<int:nro_orden>/nota_de_entrega', methods=['POST'])
# def agregar_nota_de_entrega(nro_orden):
#     data = request.json
#     fecha = data.get('fecha')
    
#     resultado = fachada_orden_compra.agregar_nota_de_entrega(nro_orden, fecha)
#     return jsonify(resultado)