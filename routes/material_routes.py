from flask import Blueprint, jsonify
from controllers.material_controller import MaterialController
from models.material.material import MaterialSchema

#DETALLE_MATERIALES
material_bp = Blueprint('material', __name__)
material_controller = MaterialController()

material_schema = MaterialSchema()
materials_schema = MaterialSchema(many = True)

@material_bp.route("/")
def inicio():
    return "INICIO"

#CREAR MATERIAL
'''
    {
    "cod_material" : "PRUEBA",
    "descripcion": "PRUEBA",
    "existencias": 150,
    "precio_unitario": 20
    }
'''

@material_bp.route("/material", methods=['POST'])
def create():
    result = material_controller.create_material()
    if result is True:
        return jsonify({"Mensaje" : "Creado"}), 201
    
    return jsonify(result)

#OBTENER MATERIAL

@material_bp.route("/material/<int:id_material>", methods=['GET'])
def obtener_material(id_material):
    result = material_controller.get_material(id_material)
    
    if not result:
        return jsonify({'error': 'Material no encontrado'}), 404
    
    return material_schema.jsonify(result)

#OBTENER MATERIALES

@material_bp.route("/materiales", methods=['GET'])
def obtener_materiales():
    results = material_controller.get_materiales()
    if not materials_schema.dump(results):
        return jsonify({"Mensaje" : "No hay materiales"})
    return jsonify({"materiales" : materials_schema.dump(results)})

#ACTUALIZAR PARCIALMENTE "PUT"

'''
    cuerpo
    {
    "cod_material" : "ACT-PRUEBA",
    "descripcion": "ACT PRUEBA",
    "existencias": 1,
    "precio_unitario": 1
    }
'''

@material_bp.route("/material/<int:id_material>", methods=['PUT'])
def actualizar_campos(id_material):
    updated_material = material_controller.update_material(id_material)

    if updated_material is None:
        return jsonify({'error': 'Material not found or update failed'}), 404

    return material_schema.jsonify(updated_material)

'''
    Response
    {
    "ID_material": 7,
    "cod_material": "ACT-PRUEBA",
    "descripcion": "ACT PRUEBA",
    "existencias": 1.0,
    "precio_unitario": 1.0
    }
'''

#ELIMINAR

@material_bp.route("/material/<int:material_id>", methods=['DELETE'])
def eliminar_material(material_id):
    deleted_material = material_controller.delete_material(material_id)

    if deleted_material is None:
        return jsonify({'error': 'Material not found or update failed'}), 404
    
    return jsonify({"Mensaje" : "Eliminado"}), 200
