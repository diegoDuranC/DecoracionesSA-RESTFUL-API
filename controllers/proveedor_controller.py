from models.proveedor import Proveedor
from app import db
from flask import request

class ProveedorController():
    
    def create_proveedor(self):
        request_data = request.get_json()
        proveedor = Proveedor(**request_data)

        db.session.add(proveedor)
        db.session.commit()

        return proveedor
    
    def get_proveedores(self):
        return Proveedor.query.all()
    
    def get_proveedor(self, id):
        proveedor = Proveedor.query.get(id)

        if proveedor is None:
            return None
        
        return proveedor

    def update_proveedor(self, id):
        proveedor = Proveedor.query.get(id)

        if proveedor is None:
            return None
        
        if 'nombre' in request.json: proveedor.nombre = request.json['nombre']
        if 'telefono' in request.json: proveedor.telefono = request.json['telefono']
        if 'empresa' in request.json: proveedor.empresa = request.json['empresa']
        if 'direccion' in request.json: proveedor.direccion = request.json['direccion']

        db.session.commit()

        return proveedor
    
    def delete_proveedor(self, id):
        proveedor = Proveedor.query.get(id)

        if proveedor is None:
            return None
        
        db.session.delete(proveedor)
        db.session.commit()

        return proveedor