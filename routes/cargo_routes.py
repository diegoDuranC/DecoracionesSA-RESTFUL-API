from flask import Blueprint, jsonify, request
from controllers.cargo_controller import CargoController
from models.rrhh.cargo import CargoSchema
from flask_cors import cross_origin

cargo_bp = Blueprint('cargo', __name__)
cargo_controller = CargoController()

cargo_schema = CargoSchema()
cargo_schemas = CargoSchema(many=True)

'''
{
    "cargo" : "VENDEDOR",
    "cod_cargo" : "VENVEND"
}

{
        "cargo": "prueba",
        "cod_cargo": "codprueba"
}
'''

@cargo_bp.route("/cargo", methods=['POST'])
def crear():
    result = cargo_controller.create_cargo()
    return cargo_schema.jsonify(result)

#OBTENER CARGO
@cargo_bp.route("/cargo/<int:id_cargo>", methods=['GET'])
def obtener_cargo(id_cargo):
    result = cargo_controller.get_cargo(id_cargo)

    if not result:
        return jsonify({'error': 'Cargo no encontrado'}), 404
    
    return cargo_schema.jsonify(result)

#OBTENER CARGOS

@cargo_bp.route("/cargos", methods=['GET'])
def obtener_cargos():
    results = cargo_controller.get_cargos()
    cargo_schema.dump(results)

    return cargo_schemas.jsonify(results)

#ACTUALIZAR PARCIALMENTE "PUT"

'''
{
    "cargo" : "VENDEDOR",
    "cod_cargo" : "VENVEND"
}

'''
@cargo_bp.route("/cargo/<int:id_cargo>", methods=['PUT'])
def actualizar_campos(id_cargo):
    updated_cargo = cargo_controller.update_cargo(id_cargo)

    if updated_cargo is None:
        return jsonify({'error': 'Cargo no encontrado o actualización fallida'}), 404

    return cargo_schema.jsonify(updated_cargo)

#ELIMINAR
@cargo_bp.route("/cargo/<int:id_cargo>", methods=['DELETE'])
def eliminar_cargo(id_cargo):
    deleted_cargo = cargo_controller.delete_cargo(id_cargo)

    if deleted_cargo is None:
        return jsonify({'error': 'Cargo not found or update failed'}), 404
    
    return jsonify(deleted_cargo)

#Cargo por codigo de cargo
#enviar por args el cod_cargo

'''
    args
    cod_cargo = "string cod cargo"
'''
@cargo_bp.route("/cargo/cod_cargo", methods=['GET'])
def obtener_cargo_cod():
    cod_cargo = request.args.get('cod_cargo')
    
    result = cargo_controller.get_cargo_cod(cod_cargo=cod_cargo)

    if result is None:
        return jsonify({'error': 'Cargo no encontrado'}), 404
    
    return cargo_schema.jsonify(result)

'''
Respuesta
{
    "cargo": "ARQUITECTO",
    "cod_cargo": "DECARQ",
    "id_cargo": 1
}
'''