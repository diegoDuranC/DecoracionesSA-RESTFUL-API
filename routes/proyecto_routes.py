from flask import Blueprint, jsonify
from flask_cors import cross_origin

from controllers.proyecto_controller import ProyectoController
from models.proyecto import ProyectoSchema

proyecto_controller = ProyectoController()
proyecto_schema = ProyectoSchema()
proyecto_schemas = ProyectoSchema(many=True)

proyecto_bp = Blueprint('proyecto', __name__)


@proyecto_bp.route("/proyecto", methods=['POST'])
def crear():
    result = proyecto_controller.create_proyecto()
    return proyecto_schema.jsonify(result)


@proyecto_bp.route("/proyectos", methods=['GET'])
def obtener_proyectos():
    results = proyecto_controller.get_proyectos()
    proyecto_schemas.dump(results)

    return proyecto_schemas.jsonify(results)

@proyecto_bp.route("/proyecto/<int:id_proyecto>", methods=['GET'])
def obtener_proyecto(id_proyecto):
    
    result = proyecto_controller.get_proyecto(id_proyecto)

    if result is None:
        return jsonify({'error': 'Proyecto no encontrado'})
    
    return proyecto_schema.jsonify(result)

@proyecto_bp.route("/proyecto/<int:id_proyecto>", methods=['PUT'])
def actualizar_proyecto(id_proyecto):
    updated_proyecto = proyecto_controller.update_proyecto(id_proyecto)

    if updated_proyecto is None:
        return jsonify({'error': 'Proyecto no encontrado'})
    
    return proyecto_schema.jsonify(updated_proyecto)

@proyecto_bp.route("/proyecto/<int:nro_proyecto>", methods=['DELETE'])
def eliminar_proyecto(nro_proyecto):
    deleted_proyecto = proyecto_controller.delete_proyecto(nro_proyecto)

    if deleted_proyecto is None:
        return jsonify({'error': 'Proyecto no encontrado'})
    
    return proyecto_schema.jsonify(deleted_proyecto)
