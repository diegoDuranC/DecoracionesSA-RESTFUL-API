from flask import Blueprint, jsonify, request
from controllers.banco_controller import BancoController
from models.banco.banco import BancoSchema
from flask_cors import cross_origin

banco_bp = Blueprint('banco', __name__)
banco_controller = BancoController()

banco_schema = BancoSchema()
banco_schemas = BancoSchema(many=True)

#CREAR UN BANCO
@banco_bp.route("/banco", methods=['POST'])
def crear():
    request_data = request.get_json()
    result = banco_controller.create_banco(request_data=request_data)
    return jsonify(result)

#OBTEN TODOS LOS BANCOS
@banco_bp.route("/bancos", methods=['GET'])
def obtener_bancos():
    result = banco_controller.get_bancos()
    banco_schemas.dump(result)

    return banco_schemas.jsonify(result)

#OBTIENE UN BANCO POR SU ID
@banco_bp.route("/banco/<int:banco_id>", methods=['GET'])
def obtener_banco(banco_id):
    result = banco_controller.get_banco(banco_id)

    if not result:
        return jsonify({'error': 'Banco no encontrado'}), 404

    return banco_schema.jsonify(result)

#OBTIENE UN BANCO POR COD BANCO
@banco_bp.route("/banco/cod_banco", methods=['GET'])
def obtener_banco_cod_banco():
    cod_banco = request.args.get('cod_banco')
    result = banco_controller.get_banco_cod_banco(cod_banco=cod_banco)

    return jsonify(result)

#ACTUALIZA UN BANCO POR SU ID
@banco_bp.route("/banco/<int:banco_id>", methods=['PUT'])
def actualizar_campos(banco_id):
    updated_banco = banco_controller.update_banco(banco_id)

    if updated_banco is None:
        return jsonify({'error': 'Banco no encotrado o actualización fallida'}), 404

    return banco_schema.jsonify(updated_banco)

#ELIMINA UN BANCO POR SU ID
@banco_bp.route("/banco/<int:banco_id>", methods=['DELETE'])
def eliminar_banco(banco_id):
    deleted_banco = banco_controller.delete_banco(banco_id)

    if deleted_banco is None:
        return jsonify({'error': 'Banco not found or update failed'}), 404
    
    return banco_schema.jsonify(deleted_banco)

