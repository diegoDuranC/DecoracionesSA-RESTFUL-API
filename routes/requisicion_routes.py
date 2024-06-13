from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from controllers.requisicion_controller import RequisicionController
from models.requisicion.requisicion import RequisicionSchema, SingleRequisicionSchema
from services.facades.requisicion_facade import RequisicionFacade

requisicion_bp = Blueprint('requisicion', __name__)

requisicion_controller = RequisicionController()

requisicion_schema = RequisicionSchema()
requisicion_schemas = RequisicionSchema(many=True)

single_requisicion_schema = SingleRequisicionSchema()
single_requisicion_schemas = SingleRequisicionSchema(many=True)

requisicion_facade = RequisicionFacade()

'''
    Ejemplo body
    
    {
    "fecha_entrega_requerida": "2024-06-30",
    "descripcion": "Requisición de materiales para proyecto X",
    "costo": 5000,
    "proyecto_nro_proyecto": 1,
    "materiales_solicitados": [
        {
            "id_material": 1,
            "cantidad_solicitada": 10
        },
        {
            "id_material": 2,
            "cantidad_solicitada": 5
        }
    ]
}

'''

@requisicion_bp.route("/requisicion", methods=['POST'])
def crear():
    request_data = request.get_json()
    result = requisicion_facade.crear_requisicion(request_data)

    if result is True:
        return jsonify({"Mensaje" : "Creado"}), 201

    return jsonify(result)

'''
    Agrega nuevos detalles a la requisicion
    Ejemplo de json:
    [
        {
            "id_material": 1,
            "cantidad_solicitada": 10
        },
        {
            "id_material": 2,
            "cantidad_solicitada": 10
        }
]
'''
@requisicion_bp.route("/requisicion/<int:nro_requisicion>/detalle", methods=['POST'])
def agregar_detalle_a_requisicion(nro_requisicion):
    request_data = request.get_json()
    resultado = requisicion_facade.agregar_detalle_a_requisicion(nro_requisicion, request_data)
    return jsonify(resultado)

'''
    [
    {
        "costo": "5000.00",
        "descripcion": "Requisición de materiales para proyecto 2",
        "fecha_creacion": "2024-06-10",
        "fecha_entrega_requerida": "2024-06-30",
        "materiales_solicitados": [
            {
                "ID": 16,
                "cantidad_solicitada": 10.0,
                "id_material": 1,
                "material": {
                    "descripcion": "Madera Roble",
                    "precio_unitario": 20.0
                }
            }
        ],
        "nro_requisicion": 24,
        "proyecto": {
            "cliente": {
                "apellido_cliente": "Chacon",
                "direccion_cliente": "B/ La Chacarilla",
                "nombre_cliente": "Lucas",
                "telefono_cliente": "7712988"
            },
            "cod_proyecto": "DEC7607474-2",
            "descripcion_proyecto": "Desripcion",
            "encargado": {
                "apellido": "LOPEZ ALVARADO",
                "nombre": "LUIS ENRIQUE"
            },
            "nombre_proyecto": "Proyecto 2",
            "nro_proyecto": 2
        }
    },
    {
        "costo": "5000.00",
        "descripcion": "Requisición de materiales para proyecto 2",
        "fecha_creacion": "2024-06-10",
        "fecha_entrega_requerida": "2024-06-30",
        "materiales_solicitados": [
            {
                "ID": 17,
                "cantidad_solicitada": 10.0,
                "id_material": 1,
                "material": {
                    "descripcion": "Madera Roble",
                    "precio_unitario": 20.0
                }
            },
            {
                "ID": 18,
                "cantidad_solicitada": 10.0,
                "id_material": 2,
                "material": {
                    "descripcion": "Madera Pino",
                    "precio_unitario": 20.0
                }
            }
        ],
        "nro_requisicion": 25,
        "proyecto": {
            "cliente": {
                "apellido_cliente": "Chacon",
                "direccion_cliente": "B/ La Chacarilla",
                "nombre_cliente": "Lucas",
                "telefono_cliente": "7712988"
            },
            "cod_proyecto": "DEC7607474-2",
            "descripcion_proyecto": "Desripcion",
            "encargado": {
                "apellido": "LOPEZ ALVARADO",
                "nombre": "LUIS ENRIQUE"
            },
            "nombre_proyecto": "Proyecto 2",
            "nro_proyecto": 2
        }
    }
]

    status 200 OK
'''
@requisicion_bp.route("/requisiciones", methods=['GET'])
def obtener_requisiciones_s():
    results = requisicion_facade.get_requisiciones()
    return jsonify(results)

#FACADE
'''
    Obtiene una requisicion por su nro de requisicion
'''
@requisicion_bp.route("/requisicion/<int:nro_requisicion>", methods=['GET'])
def obtener_requisicion(nro_requisicion):
    result = requisicion_facade.get_requisicion(nro_requisicion)

    if result is None : return jsonify({'error' : 'Requisicion no encontrada'}), 404
    result = requisicion_schema.dump(result)
    
    return requisicion_schema.jsonify(result)

'''
    Eliminar una requisicion por su nro de requisicion
'''
@requisicion_bp.route("/requisicion/<int:nro_requisicion>", methods=['DELETE'])
def eliminar_requisicione(nro_requisicion):
    query = requisicion_facade.eliminar_requisicion(nro_requisicion=nro_requisicion)

    if query is None:
        return jsonify({'Error': 'Requisición no encontrada'}), 404

    return jsonify(query)


'''
    {
    "fecha_entrega_requerida": "2024-08-10",
    "descripcion": "Cuerpo Actualizado Rerquisicion de PRUEBA proyecto 3",
    "costo": 100,
    "proyecto_nro_proyecto": 3
}
'''
@requisicion_bp.route("/requisicion/<int:nro_requisicion>", methods=['PUT'])
def actualizar_encabezado_requisicion(nro_requisicion):
    request_data = request.get_json()
    result = requisicion_facade.actualizar_encabezado_requisicion(nro_requisicion, request_data)
    return jsonify(result)

'''
Actualiza los detalles de una requisicion, recibe el nro de la requisicion como parametro de URL

JSON esperado:
{
    "materiales_solicitados": [
        {
            "ID": 1,
            "cantidad_solicitada": 15
        },
        {
            "ID": 2,
            "cantidad_solicitada": 20
        },
        {
            "ID": 3,
            "cantidad_solicitada": 25
        }
    ]
}

Donde ID es el id de la instancia de detalle, no del material

'''
@requisicion_bp.route("/requisicion/<int:nro_requisicion>/detalle", methods=['PUT'])
def actualizar_detalles_requisicion(nro_requisicion):
    request_data = request.get_json()
    result = requisicion_facade.actualizar_detalles_requisicion(nro_requisicion, request_data)
    return jsonify(result)

'''
    Elimina un registro de detalle, uno por uno

'''
@requisicion_bp.route("/requisicion/<int:nro_requisicion>/detalle/<int:id_detalle>", methods=['DELETE'])
def eliminar_campo_detalles_requisicion(nro_requisicion, id_detalle):
    result = requisicion_facade.eliminar_detalle_requisicion(nro_requisicion=nro_requisicion, id_detalle=id_detalle)

    return jsonify(result)