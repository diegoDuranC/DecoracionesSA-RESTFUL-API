from flask import Blueprint, jsonify
from flask_cors import cross_origin

from controllers.proyecto_controller import ProyectoController

proyecto_controller = ProyectoController()

proyecto_bp = Blueprint('proyecto', __name__)

@proyecto_bp.route("/ruta_prueba", methods=['GET'])
def mensaje():
    return jsonify({"Mensaje" : "Correcto"})


'''
{
    "cod_proyecto": "codigoprueba",
    "nombre_proyecto": "Proyecto 4 Prueba",
    "desripcion": "Descripcion",
    "cod_cliente": "CLI-7607474",
    "cod_empleado": "PRO-3087098"
}
'''
@proyecto_bp.route("/proyecto", methods=['POST'])
def crear():
    result = proyecto_controller.create_proyecto()
    if result is True:
        return jsonify({"Message" : "Creado"}), 201
    
    return jsonify(result)


@proyecto_bp.route("/proyectos", methods=['GET'])
def obtener_proyectos():
    results = proyecto_controller.get_proyectos()

    return jsonify(results)

@proyecto_bp.route("/proyecto/<int:id_proyecto>", methods=['GET'])
def obtener_proyecto(id_proyecto):
    
    result = proyecto_controller.get_proyecto(id_proyecto)

    if result is None:
        return jsonify({'error': 'Proyecto no encontrado'})
    
    return jsonify(result)

@proyecto_bp.route("/proyecto/<int:id_proyecto>", methods=['PUT'])
def actualizar_proyecto(id_proyecto):
    updated_proyecto = proyecto_controller.update_proyecto(id_proyecto)

    if updated_proyecto is None:
        return jsonify({'error': 'Proyecto no encontrado'})
    
    return jsonify(updated_proyecto)

@proyecto_bp.route("/proyecto/<int:nro_proyecto>", methods=['DELETE'])
def eliminar_proyecto(nro_proyecto):
    deleted_proyecto = proyecto_controller.delete_proyecto(nro_proyecto)

    if deleted_proyecto is None:
        return jsonify({'Error': 'Proyecto no encontrado'})
    
    if deleted_proyecto is True:
        return jsonify({"Mensaje" : "Eliminado"}), 200
    
    return jsonify(deleted_proyecto)


##RUTA PARA OBTENER LOS COORDINADORES PARA PROYECTOS