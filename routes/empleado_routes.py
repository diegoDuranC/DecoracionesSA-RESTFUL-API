from flask import Blueprint, jsonify, request
from controllers.empleado_controller import EmpleadoController

empleado_bp = Blueprint('empleado', __name__)
empleado_controller = EmpleadoController()

# EJEMPLO CUERPO JSON
'''
    {
        "ci": "3087096",
        "cod_empleado": "VEN-3087096"
        "nombre": "Luis",
        "apellido": "Lopez Alvarado",
        "telefono": "73274099",
        "cargo_id": 3,  
        "departamento_id": 11, 
    }
'''

@empleado_bp.route("/empleado", methods=['POST'])
def crear():
    query = empleado_controller.create_empleado()

    if query is True:
        return jsonify({"Mensaje" : "Empleado creado"}), 201
    
    return jsonify(query)

'''
    {
        "ci": "3087096",
        "nombre": "Luis",
        "apellido": "Lopez Alvarado",
        "telefono": "73274099",
        "cargo": "Ayudante",
        "departamento_id": 1  
    }
'''

@empleado_bp.route("/empleado/<int:id_empleado>", methods=['GET'])
def obtener_empleado(id_empleado):
    result = empleado_controller.get_empleado(id_empleado)

    return jsonify(result)

@empleado_bp.route("/empleados", methods=['GET'])
def obtener_empleados():
    results = empleado_controller.get_empleados()

    return jsonify({"empleados" : results})

@empleado_bp.route("/empleado/ci", methods=['GET'])
def obtener_empleado_ci():
    ci = request.args.get("ci")
    result = empleado_controller.get_empleado_ci(ci=ci)
    return jsonify(result)

@empleado_bp.route("/empleado/<int:ID_empleado>", methods=['PUT'])
def actualizar_campos(ID_empleado):
    result = empleado_controller.update_empleado(ID_empleado)
    
    return jsonify(result)

@empleado_bp.route("/empleado/<int:ID_empleado>", methods=['DELETE'])
def eliminar_empleado(ID_empleado):
    result = empleado_controller.delete_empleado(ID_empleado)
    if result is True:
        return jsonify({"Mensaje" : "Empleado eliminado"}), 200
    
    return jsonify(result)