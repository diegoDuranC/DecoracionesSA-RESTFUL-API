from flask import Blueprint, jsonify
from controllers.area_controller import AreaController
from models.area import AreaSchema

area_bp = Blueprint('area', __name__)
area_controller = AreaController()

area_schema = AreaSchema()
area_schemas = AreaSchema(many=True)

@area_bp.route("/area", methods=['POST'])
def crear():
    result = area_controller.create_area()
    return area_schema.jsonify(result)

@area_bp.route("/areas", methods=['GET'])
def obtener_areas():
    results = area_controller.get_areas()
    area_schemas.dump(results)

    return area_schemas.jsonify(results)