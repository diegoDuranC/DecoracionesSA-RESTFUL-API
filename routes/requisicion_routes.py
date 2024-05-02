from flask import Blueprint, jsonify
from flask_cors import cross_origin

from controllers.requisicion_controller import RequisicionController
from models.requisicion import RequisicionSchema

requisicion_bp = Blueprint('requisicion', __name__)

requisicion_controller = RequisicionController()

requisicion_schema = RequisicionSchema()
requisicion_schemas = RequisicionSchema(many=True)

@cross_origin
@requisicion_bp.route("/requisicion", methods=['POST'])
def crear():
    result = requisicion_controller.create_requisicion()
    return requisicion_schema.jsonify(result)

@cross_origin
@requisicion_bp.route("/requisiciones", methods=['GET'])
def obtener_requisiciones():
    results = requisicion_controller.get_requisiciones()
    requisicion_schemas.dump(results)

    return requisicion_schemas.jsonify(results)

@cross_origin
@requisicion_bp.route("/requisicion/<int:nro_requisicion>", methods=['GET'])
def obtener_requisicion(nro_requisicion):
    result = requisicion_controller.get_requisicion(nro_requisicion)

    if result is None : return jsonify({'error' : 'Requisicion no encontrada'}), 404

    return requisicion_schema.jsonify(result)

@cross_origin
@requisicion_bp.route("/requisicion/<int:nro_requisicion>", methods=['PUT'])
def actualizar_requisicion(nro_requisicion):
    updated_requisicion = requisicion_controller.update_requisicion(nro_requisicion)

    if updated_requisicion is None : return jsonify({'error' : 'Requisicion no encontrada'}), 404

    return requisicion_schema.jsonify(updated_requisicion)