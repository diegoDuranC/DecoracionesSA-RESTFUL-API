from models.cliente import Cliente
from app import db
from flask import request

class ClienteController():
    
    def create_cliente(self):
        request_data = request.get_json()
        cliente = Cliente(**request_data)
        db.session.add(cliente)
        db.session.commit()

        return cliente
    
    def get_cliente(self, ci_cliente):
        cliente = Cliente.query.get(ci_cliente)
        return cliente
    
    def get_clientes(self):
        return Cliente.query.all()
    
    def update_cliente(self, cliente_ci):
        cliente = Cliente.query.get(cliente_ci)

        if cliente is None:
            return None #Manejar un error de que no existe dicho objeto en la BD

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