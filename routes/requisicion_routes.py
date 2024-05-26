from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from controllers.requisicion_controller import RequisicionController
from models.requisicion.requisicion import RequisicionSchema, SingleRequisicionSchema
from services.facades.requisicion_facade import RequisicionFacade

requisicion_bp = Blueprint('requisicion', __name__)

requisicion_controller = RequisicionController()

requisicion_schema = RequisicionSchema()
requisicion_schemas = RequisicionSchema(many=True)

single_requisicion_schema = SingleRequisicionSchema()
single_requisicion_schemas = SingleRequisicionSchema(many=True)

requisicion_facade = RequisicionFacade()


@requisicion_bp.route("/requisicion_s", methods=['POST'])
def crear():
    request_data = request.get_json()
    result = requisicion_facade.crear_requisicion(request_data)

    return requisicion_schema.jsonify(result)


@requisicion_bp.route("/requisiciones_s", methods=['GET'])
def obtener_requisiciones_s():
    results = requisicion_controller.get_requisiciones()
    single_requisicion_schemas.dump(results)

    return single_requisicion_schemas.jsonify(results)

@requisicion_bp.route("/requisicion_s/<int:nro_requisicion>", methods=['GET'])
def obtener_requisicion_s(nro_requisicion):
    result = requisicion_controller.get_requisicion(nro_requisicion)

    if result is None : return jsonify({'error' : 'Requisicion no encontrada'}), 404

    return requisicion_schema.jsonify(result)


@requisicion_bp.route("/requisicion_s/<int:nro_requisicion>", methods=['PUT'])
def actualizar_requisicion(nro_requisicion):
    updated_requisicion = requisicion_controller.update_requisicion(nro_requisicion)

    if updated_requisicion is None : return jsonify({'error' : 'Requisicion no encontrada'}), 404

    return requisicion_schema.jsonify(updated_requisicion)

#FACADE

@requisicion_bp.route("/requisicion/<int:nro_requisicion>", methods=['GET'])
def obtener_requisicion(nro_requisicion):
    result = requisicion_facade.get_requisicion(nro_requisicion)

    if result is None : return jsonify({'error' : 'Requisicion no encontrada'}), 404
    result = requisicion_schema.dump(result)
    
    return requisicion_schema.jsonify(result)

@requisicion_bp.route("/requisiciones", methods=['GET'])
def obtener_requisiciones():
    query = requisicion_facade.get_requisiciones()
    if query is None: 
        return jsonify({"Error" : "Requisicion no encontrada"})
    return jsonify(query)