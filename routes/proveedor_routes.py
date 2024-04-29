from models.proveedor import ProveedorSchema
from flask import Blueprint, jsonify
from controllers.proveedor_controller import ProveedorController
from flask_cors import cross_origin

proveedor_bp = Blueprint('proveedor', __name__)

proveedor_controller = ProveedorController()

proveedor_schema = ProveedorSchema()
proveedor_schemas = ProveedorSchema(many=True)

@cross_origin
@proveedor_bp.route('/proveedor', methods=['POST'])
def crear():
    result = proveedor_controller.create_proveedor()
    return proveedor_schema.jsonify(result)

@cross_origin
@proveedor_bp.route('/proveedores', methods=['GET'])
def obtener_proveedores():
    results = proveedor_controller.get_proveedores()
    proveedor_schemas.dump(results)

    return proveedor_schemas.jsonify(results)


@cross_origin
@proveedor_bp.route('/proveedor/<int:nro_proveedor>', methods=['GET'])
def obtener_proveedor(nro_proveedor):
    result = proveedor_controller.get_proveedor(nro_proveedor)
    
    if not result:
        return jsonify({'error': 'Proveedor no encontrado'}), 404
    
    return proveedor_schema.jsonify(result)

@cross_origin
@proveedor_bp.route("/proveedor/<int:nro_proveedor>", methods=['PUT'])
def actualizar_campos(nro_proveedor):
    updated_proveedor = proveedor_controller.update_proveedor(nro_proveedor)

    if updated_proveedor is None:
        return jsonify({'error' : 'Proveedor no encontrado'}), 404
    
    return proveedor_schema.jsonify(updated_proveedor)

@cross_origin
@proveedor_bp.route("/proveedor/<int:nro_proveedor>", methods=['DELETE'])
def eliminar_proveedor(nro_proveedor):
    deleted_proveedor = proveedor_controller.delete_proveedor(nro_proveedor)

    if deleted_proveedor is None:
        return jsonify({'error': 'Proveedor no encontrado'}), 404
    
    return proveedor_schema.jsonify(deleted_proveedor)