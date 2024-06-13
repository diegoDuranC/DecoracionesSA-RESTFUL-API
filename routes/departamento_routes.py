from flask import Blueprint, jsonify
from controllers.departamento_controller import DepartamentoController
#from flasgger import swag_from

departamento_bp = Blueprint('departamento', __name__)
departamento_controller = DepartamentoController()

@departamento_bp.route("/departamento", methods=['POST'])
# @swag_from({
#     'responses': {
#         200: {
#             'description': 'Departamento creado exitosamente',
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'ID_departamento': {'type': 'integer'},
#                     'departamento': {'type': 'string'}
#                 }
#             }
#         }
#     },
#     'parameters': [
#         {
#             'name': 'departamento',
#             'in': 'body',
#             'type': 'string',
#             'required': True,
#             'description': 'Nombre del departamento'
#         }
#     ]
# })
def crear():
    result = departamento_controller.create_departamento()
    return jsonify(result)

@departamento_bp.route("/departamentos", methods=['GET'])
def obtener_departamentos():
    results = departamento_controller.get_departamentos()
    return jsonify({"departamentos" : results})

@departamento_bp.route("/departamento/<int:ID_departamento>", methods=['GET'])
def obtener_departamento(ID_departamento):
    result = departamento_controller.get_departamento(ID_departamento)
    return jsonify(result)

@departamento_bp.route("/departamento/<int:ID_departamento>", methods=['PUT'])
def actualizar_departamento(ID_departamento):
    updated_area = departamento_controller.update_departamento(ID_departamento)
    return jsonify(updated_area)

@departamento_bp.route("/departamento/<int:ID_departamento>", methods=['DELETE'])
def delete_departamento(ID_departamento):
    result = departamento_controller.delete_departamento(ID_departamento)
    return jsonify(result)