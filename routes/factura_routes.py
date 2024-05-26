from .cliente_routes import cliente_bp

from flask_cors import cross_origin
from flask import jsonify, request

from models.proyecto import Proyecto

from services.facades.factura_cliente_facade import FacturaClienteFacade
from models.cliente.factura_cliente import FacturaCliente, FacturaSchema

factura_schema = FacturaSchema()
factura_schemas = FacturaSchema(many=True)
factura_facade = FacturaClienteFacade()
#CREAR LA FACTURA CLIENTE
#SE NECESITA EL NUMERO DE PROYECTO PARA GENERAR LA FACTURA

@cliente_bp.route("/cliente/factura/crear_factura/<int:nro_proyecto>", methods=['GET'])
def crear_factura(nro_proyecto):
    proyecto = Proyecto.query.get(nro_proyecto)
    
    if proyecto is None:
        return jsonify({"Error": "No existe el proyecto"})
    
    factura = factura_facade.crear_factura(nro_proyecto)
    result = factura_schema.dump(factura)

    return jsonify(result)

#OBTENER FACTURAS

@cliente_bp.route("/cliente/factura/", methods=['GET'])
def obtener_factura():

    facturas = factura_facade.get_facturas()
    result = factura_schemas.dump(facturas)

    return jsonify(result)

#OBTENER FACTURAS POR CLIENTE

@cliente_bp.route("/cliente/factura/<int:id_cliente>", methods=['GET'])
def obtener_factura_cliente(id_cliente):
    
    factura = FacturaCliente.query.filter_by(cliente_id=id_cliente).first()

    if factura is None:
        return jsonify({"Error": "El cliente no tiene facturas"})

    facturas = factura_facade.get_facturas_cliente(id_cliente)
    result = factura_schemas.dump(facturas)

    return jsonify(result)