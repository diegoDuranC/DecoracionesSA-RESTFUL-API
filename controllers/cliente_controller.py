from models.cliente.cliente import Cliente
from sqlalchemy.exc import SQLAlchemyError
from app import db
from flask import request
from models.cliente.cliente import ClienteSchema


cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)

class ClienteController():
    
    def create_cliente(self):

        cod_cliente = request.json.get('cod_cliente')
        ci_cliente = request.json.get('ci_cliente')
        nombre_cliente = request.json.get('nombre_cliente')
        apellido_cliente = request.json.get('apellido_cliente')
        direccion_cliente = request.json.get('direccion_cliente')
        telefono_cliente = request.json.get('telefono_cliente')

        cliente = Cliente(
            cod_cliente = cod_cliente,
            ci_cliente=ci_cliente,
            nombre_cliente=nombre_cliente,
            apellido_cliente=apellido_cliente,
            direccion_cliente=direccion_cliente,
            telefono_cliente=telefono_cliente
        )

        try:
            db.session.add(cliente)
            db.session.commit()

            return True
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"Error": str(e)}
    
    def get_cliente_ci(self, ci_cliente):
        #cliente = Cliente.query.get(ci_cliente)
        cliente = Cliente.query.filter_by(ci_cliente=ci_cliente).first()

        if cliente:
            return cliente_schema.dump(cliente)
        
        return False
    
    def get_cliente_id(self, id_cliente):
        cliente = Cliente.query.get(id_cliente) 
        return cliente_schema.dump(cliente)
    
    def get_clientes(self):
        consult = Cliente.query.all()        
        return clientes_schema.dump(consult)
    
    def update_cliente(self, id_cliente):
        cliente = Cliente.query.get(id_cliente)

        if cliente is None:
            return None #Manejar un error de que no existe dicho objeto en la BD
        if 'cod_cliente' in request.json:
            cliente.cod_cliente = request.json['cod_cliente']
        if 'ci_cliente' in request.json:
            cliente.ci_cliente = request.json['ci_cliente']
        if 'nombre_cliente' in request.json:
            cliente.nombre_cliente = request.json['nombre_cliente']
        if 'apellido_cliente' in request.json:
            cliente.apellido_cliente = request.json['apellido_cliente']
        if 'direccion_cliente' in request.json:
            cliente.direccion_cliente = request.json['direccion_cliente']
        if 'telefono_cliente' in request.json:
            cliente.telefono_cliente = request.json['telefono_cliente']

        db.session.commit()

        return cliente
    
    def delete_cliente(self, id_cliente):
        cliente = Cliente.query.get(id_cliente)

        if cliente is None:
            return None

        db.session.delete(cliente)
        db.session.commit()

        return cliente