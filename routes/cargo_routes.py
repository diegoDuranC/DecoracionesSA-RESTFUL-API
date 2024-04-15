from flask import Blueprint, jsonify
from controllers.cargo_controller import CargoController
from models.cargo import CargoSchema

cargo_bp = Blueprint('cargo', __name__)
cargo_controller = CargoController()

cargo_schema = CargoSchema()
cargo_schemas = CargoSchema(many=True)

@cargo_bp.route("/cargo", methods=['POST'])
def crear():
    result = cargo_controller.create_cargo()
    return cargo_schema.jsonify(result)

#OBTENER CARGO
@cargo_bp.route("/cargo/<int:codigo_cargo>", methods=['GET'])
def obtener_cargo(codigo_cargo):
    result = cargo_controller.get_cargo(codigo_cargo)

    if not result:
        return jsonify({'error': 'Cargo no encontrado'}), 404
    
    return cargo_schema.jsonify(result)

#OBTENER CARGOS
@cargo_bp.route("/cargo", methods=['GET'])
def obtener_cargos():
    results = cargo_controller.get_cargos()
    cargo_schema.dump(results)

    return cargo_schemas.jsonify(results)

#ACTUALIZAR PARCIALMENTE "PUT"
@cargo_bp.route("/cargo/<int:codigo_cargo>", methods=['PUT'])
def actualizar_campos(codigo_cargo):
    updated_cargo = cargo_controller.update_cargo(codigo_cargo)

    if updated_cargo is None:
        return jsonify({'error': 'Cargo no encontrado o actualización fallida'}), 404

    return cargo_schema.jsonify(updated_cargo)

#ELIMINAR
@cargo_bp.route("/cargo/<int:codigo_cargo>", methods=['DELETE'])
def eliminar_cargo(codigo_cargo):
    deleted_cargo = cargo_controller.delete_cargo(codigo_cargo)

    if deleted_cargo is None:
        return jsonify({'error': 'Cargo not found or update failed'}), 404
    
    return cargo_schema.jsonify(deleted_cargo)
