from flask import Blueprint, jsonify, request
from controllers.cliente_controller import ClienteController
from models.cliente.cliente import ClienteSchema

from flask_cors import cross_origin

cliente_bp = Blueprint('cliente', __name__)
cliente_controller = ClienteController()

cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)

#Crear Cliente

'''
    {
            "apellido_cliente": "Chacon",
            "ci_cliente": "7607474",
            "cod_cliente": "CLI-7607474",
            "direccion_cliente": "B/ La Chacarilla",
            "nombre_cliente": "Lucas",
            "telefono_cliente": "7712988"
    }
'''
@cliente_bp.route("/cliente", methods=['POST'])
def create():
    result = cliente_controller.create_cliente()
    if result is True:
        return jsonify({"Mensaje" : "Creado"}), 201
    
    return jsonify(result)

#OBTENER CLIENTE CI
#Enviar en los Query Params
# ci_cliente = str() -> String del ci del cliente

@cliente_bp.route("/cliente/ci", methods=['GET'])
def obtener_cliente_ci():

    ci_cliente = request.args.get('ci')
    result = cliente_controller.get_cliente_ci(ci_cliente)
    
    if result is False:
        return jsonify({"Error" : "cliente no encontrado"}), 404
    
    return jsonify(result)

#OBTENER CLIENTE POR ID

@cliente_bp.route("/cliente/<int:id_cliente>", methods=['GET'])
def obtener_cliente_id(id_cliente):
    result = cliente_controller.get_cliente_id(id_cliente)

    if not result:
        return jsonify({'error': 'Cliente no encontrado'}), 404
    
    return cliente_schema.jsonify(result)

#OBTENER CLIENTES

@cliente_bp.route("/clientes", methods=['GET'])
def obtener_clientes():
    results = cliente_controller.get_clientes()

    return jsonify({"clientes" : results})

'''
    Respuesta:
    {
        "clientes": [
            {
                "ID_cliente": 1,
                "apellido_cliente": "Chacon",
                "ci_cliente": "7607474",
                "cod_cliente": "CLI-7607474",
                "direccion_cliente": "B/ La Chacarilla",
                "nombre_cliente": "Lucas",
                "telefono_cliente": "7712988"
            },
            {
                "ID_cliente": 5,
                "apellido_cliente": "Perez",
                "ci_cliente": "1076565",
                "cod_cliente": "CLI-1076565",
                "direccion_cliente": "B/ La Chacarilla",
                "nombre_cliente": "Mateo",
                "telefono_cliente": "72175033"
            }
        ]
    }

    ID_cliente es el id de la instacia es un autoincrement, es la pk
'''

# #ACTUALIZAR PARCIALMENTE "PUT"
'''
    {
            "apellido_cliente": "Chacon",
            "ci_cliente": "7607474",
            "cod_cliente": "CLI-7607474",
            "direccion_cliente": "B/ La Chacarilla",
            "nombre_cliente": "Lucas",
            "telefono_cliente": "7712988"
    }
'''

@cliente_bp.route("/cliente/<int:id_cliente>", methods=['PUT'])
def actualizar_campos(id_cliente):
    updated_cliente = cliente_controller.update_cliente(id_cliente)

    if updated_cliente is None:
         return jsonify({'error': 'Client not found or update failed'}), 404

    return cliente_schema.jsonify(updated_cliente)

#ELIMINAR

@cliente_bp.route("/cliente/<int:id_cliente>", methods=['DELETE'])
def eliminar_cliente(id_cliente):
    deleted_cliente = cliente_controller.delete_cliente(id_cliente)

    if deleted_cliente is None:
        return jsonify({'error': 'Material not found or update failed'}), 404
    
    return cliente_schema.jsonify(deleted_cliente)
