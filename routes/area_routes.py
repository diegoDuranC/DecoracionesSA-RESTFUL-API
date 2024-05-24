from flask import Blueprint, jsonify
from controllers.area_controller import AreaController
from models.rrhh.area import AreaSchema
from flask_cors import cross_origin

area_bp = Blueprint('area', __name__)
area_controller = AreaController()

area_schema = AreaSchema()
area_schemas = AreaSchema(many=True)

@cross_origin()
@area_bp.route("/area", methods=['POST'])
def crear():
    result = area_controller.create_area()
    return area_schema.jsonify(result)

@cross_origin()
@area_bp.route("/areas", methods=['GET'])
def obtener_areas():
    results = area_controller.get_areas()
    area_schemas.dump(results)

    return area_schemas.jsonify(results)

@cross_origin()
@area_bp.route("/area/<int:cod_area>", methods=['GET'])
def obtener_area(cod_area):
    result = area_controller.get_area(cod_area)

    if result is None:
        return jsonify({'error': 'Area no encontrada'})

    return area_schema.jsonify(result)

@cross_origin
@area_bp.route("/area/<int:cod_area>", methods=['PUT'])
def actualizar_area(cod_area):
    updated_area = area_controller.update_area(cod_area)
    return area_schema.jsonify(updated_area)

@cross_origin
@area_bp.route("/area/<int:cod_area>", methods=['DELETE'])
def delete_area(cod_area):
    deleted_area = area_controller.delete_area(cod_area)
    return area_schema.jsonify(deleted_area)