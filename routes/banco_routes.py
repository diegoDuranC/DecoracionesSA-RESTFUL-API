from flask import Blueprint, jsonify
from controllers.banco_controller import BancoController
from models.banco.banco import BancoSchema
from flask_cors import cross_origin

banco_bp = Blueprint('banco', __name__)
banco_controller = BancoController()

banco_schema = BancoSchema()
banco_schemas = BancoSchema(many=True)

@cross_origin
@banco_bp.route("/banco", methods=['POST'])
def crear():
    result = banco_controller.create_banco()
    return banco_schema.jsonify(result)

@cross_origin
@banco_bp.route("/bancos", methods=['GET'])
def obtener_bancos():
    result = banco_controller.get_bancos()
    banco_schemas.dump(result)

    return banco_schemas.jsonify(result)

@cross_origin
@banco_bp.route("/banco/<int:banco_id>", methods=['GET'])
def obtener_banco(banco_id):
    result = banco_controller.get_banco(banco_id)

    if not result:
        return jsonify({'error': 'Banco no encontrado'}), 404

    return banco_schema.jsonify(result)

@cross_origin()
@banco_bp.route("/banco/<int:banco_id>", methods=['PUT'])
def actualizar_campos(banco_id):
    updated_banco = banco_controller.update_banco(banco_id)

    if updated_banco is None:
        return jsonify({'error': 'Banco no encotrado o actualización fallida'}), 404

    return banco_schema.jsonify(updated_banco)

@cross_origin
@banco_bp.route("/banco/<int:banco_id>", methods=['DELETE'])
def eliminar_banco(banco_id):
    deleted_banco = banco_controller.delete_banco(banco_id)

    if deleted_banco is None:
        return jsonify({'error': 'Banco not found or update failed'}), 404
    
    return banco_schema.jsonify(deleted_banco)

