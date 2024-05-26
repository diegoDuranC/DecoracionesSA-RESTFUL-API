from flask import Blueprint, jsonify
from controllers.empleado_controller import EmpleadoController
from models.rrhh.empleado import EmpleadoSchema
from flask_cors import cross_origin

empleado_bp = Blueprint('empleado', __name__)
empleado_controller = EmpleadoController()

empleado_schema = EmpleadoSchema()
empleado_schemas = EmpleadoSchema(many=True)

'''
    {
        "ci_empleado": "3087096",
        "nombre_empleado": "Luis",
        "apellido_empleado": "Lopez Alvarado",
        "telefono_empleado": "73274099",
        "fecha_contratacion": "2018-02-12",
        "fecha_despido": null o "YYYY-mm-dd"
        "cargo_id": 9,  
        "area_id": 11,  
        "jefe_id": 4  
    }
'''


@empleado_bp.route("/empleado", methods=['POST'])
def crear():
    empleado = empleado_controller.create_empleado()

    # if not empleado:
    #     return 404
    
    return empleado_schema.jsonify(empleado)

'''
    {
        "ci_empleado": "3087096",
        "nombre_empleado": "Luis",
        "apellido_empleado": "Lopez Alvarado",
        "telefono_empleado": "73274099",
        "fecha_contratacion": "2018-02-12",
        "fecha_despido": null o "YYYY-mm-dd"
        "cargo_id": 9,  
        "area_id": 11,  
        "jefe_id": 4  
    }
'''


@empleado_bp.route("/empleado/<int:id_empleado>", methods=['PUT'])
def actualizar_campos(id_empleado):
    updated_empleado = empleado_controller.update_empleado(id_empleado)

    if updated_empleado is None: 
        return jsonify({'error': 'Cargo no encontrado o actualización fallida'}), 404
    
    return empleado_schema.jsonify(updated_empleado)


@empleado_bp.route("/empleado/<int:id_empleado>", methods=['GET'])
def obtener_empleado(id_empleado):
    result = empleado_controller.get_empleado(id_empleado)

    return empleado_schema.jsonify(result)


@empleado_bp.route("/empleados", methods=['GET'])
def obtener_empleados():
    results = empleado_controller.get_empleados()
    empleado_schemas.dump(results)

    return empleado_schemas.jsonify(results)