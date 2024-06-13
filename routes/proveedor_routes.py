from models.proveedor import ProveedorSchema
from flask import Blueprint, jsonify, request
from controllers.proveedor_controller import ProveedorController
from flask_cors import cross_origin

proveedor_bp = Blueprint('proveedor', __name__)

proveedor_controller = ProveedorController()

proveedor_schema = ProveedorSchema()
proveedor_schemas = ProveedorSchema(many=True)


'''
    El codigo yo lo manejo por las siglas de la empresa y el numero del encargado o el proveedor
    {
        "nombre" : "Proveedor de Prueba",
        "telefono": "11111111",
        "empresa": "ABC",
        "direccion": "Calle XYZ",
        "cod_proveedor": "FT-11111111"
    }
'''
#CREAR UN PROVEEDOR
@proveedor_bp.route('/proveedor', methods=['POST'])
def crear():
    result = proveedor_controller.create_proveedor()
    return jsonify(result)

#OBTIENE TODOS LOS PROVEEDORES
@proveedor_bp.route('/proveedores', methods=['GET'])
def obtener_proveedores():
    results = proveedor_controller.get_proveedores()
    proveedor_schemas.dump(results)

    return proveedor_schemas.jsonify(results)

#OBTIENE PROVEEDOR POR ID PROVEEDOR
@proveedor_bp.route('/proveedor/<int:id_proveedor>', methods=['GET'])
def obtener_proveedor(id_proveedor):
    result = proveedor_controller.get_proveedor(id_proveedor)
    
    if not result:
        return jsonify({'error': 'Proveedor no encontrado'})
    
    return proveedor_schema.jsonify(result)

'''
    Obtiene el proveedor por args de params
    EJEMPLO RUTA http://25.5.250.33:5000/proveedor/cod_proveedor?cod_proveedor=FT-11111111

    cod_proveedor = FT-11111111
'''
#OBTIENE PROVEEDOR POR COD PROVEEDOR
@proveedor_bp.route("/proveedor/cod_proveedor", methods=['GET'])
def obtener_proveedor_cod_proveedor():
    cod_proveedor = request.args.get('cod_proveedor')
    result = proveedor_controller.get_proovedor_cod_proveedor(cod_proveedor=cod_proveedor)
    return proveedor_schema.jsonify(result)

'''
    {
        "cod_proveedor": "FT-11111111",
        "direccion": "Calle ABC",
        "empresa": "XYZ",
        "id_proveedor": 2,
        "nombre": "Proveedor de Prueba Actualizado",
        "telefono": "11111111"
    }
'''
#ACTUALIZAR EL PROVEEDOR
@proveedor_bp.route("/proveedor/<int:id_proveedor>", methods=['PUT'])
def actualizar_campos(id_proveedor):
    updated_proveedor = proveedor_controller.update_proveedor(id_proveedor)

    if updated_proveedor is None:
        return jsonify({'error' : 'Proveedor no encontrado'}), 404
    
    return proveedor_schema.jsonify(updated_proveedor)

#ELIMINAR EL PROVEEDOR
@proveedor_bp.route("/proveedor/<int:id_proveedor>", methods=['DELETE'])
def eliminar_proveedor(id_proveedor):
    deleted_proveedor = proveedor_controller.delete_proveedor(id_proveedor)

    if deleted_proveedor is None:
        return jsonify({'error': 'Proveedor no encontrado'}), 404
    
    return jsonify(deleted_proveedor)