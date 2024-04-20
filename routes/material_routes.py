from flask import Blueprint, jsonify
from controllers.material_controller import MaterialController
from models.material import MaterialSchema
from flask_cors import cross_origin

material_bp = Blueprint('material', __name__)
material_controller = MaterialController()

material_schema = MaterialSchema()
materials_schema = MaterialSchema(many = True)

#CREAR MATERIAL
@cross_origin()
@material_bp.route("/material", methods=['POST'])
def create():
    result = material_controller.create_material()
    return material_schema.jsonify(result)

# ##################PROBAR##################
# #CREAR MATERIALES 
# @material_bp.route("/materiales", methods=['POST'])
# def create_materiales():
#     results = material_controller.create_materiales()
#     return materials_schema.jsonify(results)

#OBTENER MATERIAL
@cross_origin()
@material_bp.route("/material/<int:codigo_material>", methods=['GET'])
def obtener_material(codigo_material):
    result = material_controller.get_material(codigo_material)
    
    if not result:
        return jsonify({'error': 'Material no encontrado'}), 404
    
    return material_schema.jsonify(result)

#OBTENER MATERIALES
@cross_origin()
@material_bp.route("/materiales", methods=['GET'])
def obtener_materiales():
    results = material_controller.get_materiales()
    materials_schema.dump(results)

    return materials_schema.jsonify(results)

#ACTUALIZAR PARCIALMENTE "PUT"
@cross_origin()
@material_bp.route("/material/<int:codigo_material>", methods=['PUT'])
def actualizar_campos(codigo_material):
    updated_material = material_controller.update_material(codigo_material)

    if updated_material is None:
        return jsonify({'error': 'Material not found or update failed'}), 404

    return material_schema.jsonify(updated_material)

#ELIMINAR
@cross_origin()
@material_bp.route("/material/<int:codigo_material>", methods=['DELETE'])
def eliminar_material(codigo_material):
    deleted_material = material_controller.delete_material(codigo_material)

    if deleted_material is None:
        return jsonify({'error': 'Material not found or update failed'}), 404
    
    return material_schema.jsonify(deleted_material)