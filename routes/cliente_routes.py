from flask import Blueprint, jsonify
from controllers.cliente_controller import ClienteController
from models.cliente import ClienteSchema

cliente_bp = Blueprint('cliente', __name__)
cliente_controller = ClienteController()

cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)

#Crear Cliente
@cliente_bp.route("/cliente", methods=['POST'])
def create():
    result = cliente_controller.create_cliente()
    return cliente_schema.jsonify(result)

##################PROBAR##################
#CREAR MATERIALES 
# @cliente_bp.route("/clientes", methods=['POST'])
# def create_materiales():
#     results = material_controller.create_materiales()
#     return materials_schema.jsonify(results)

#OBTENER CLIENTE
@cliente_bp.route("/cliente/<string:ci_cliente>", methods=['GET'])
def obtener_material(ci_cliente):
    result = cliente_controller.get_cliente(ci_cliente)

    if not result:
        return jsonify({'error': 'Cliente no encontrado'}), 404
    
    return cliente_schema.jsonify(result)

#OBTENER CLIENTES
@cliente_bp.route("/clientes", methods=['GET'])
def obtener_materiales():
    results = cliente_controller.get_clientes()
    clientes_schema.dump(results)

    return clientes_schema.jsonify(results)

# #ACTUALIZAR PARCIALMENTE "PUT"
@cliente_bp.route("/cliente/<int:id_cliente>", methods=['PUT'])
def actualizar_campos(id_cliente):
    updated_cliente = cliente_controller.update_cliente(id_cliente)

    if updated_cliente is None:
         return jsonify({'error': 'Client not found or update failed'}), 404

    return cliente_schema.jsonify(updated_cliente)

#ELIMINAR
@cliente_bp.route("/cliente/<int:id_cliente>", methods=['DELETE'])
def eliminar_material(id_cliente):
    deleted_cliente = cliente_controller.delete_cliente(id_cliente)

    if deleted_cliente is None:
        return jsonify({'error': 'Material not found or update failed'}), 404
    
    return cliente_schema.jsonify(deleted_cliente)