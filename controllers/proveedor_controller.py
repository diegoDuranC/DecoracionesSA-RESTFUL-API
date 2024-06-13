from models.proveedor import Proveedor
from app import db
from flask import request

class ProveedorController():
    
    def create_proveedor(self):
        request_data = request.get_json()

        cod_proveedor = request_data.get('cod_proveedor')
        nombre = request_data.get('nombre')
        telefono  = request_data.get('telefono')
        empresa  = request_data.get('empresa')
        direccion  = request_data.get('direccion')
        cod_prov = cod_proveedor.upper()

        try:    
            proveedor = Proveedor(
                cod_proveedor=cod_prov,
                nombre=nombre,
                telefono=telefono,
                empresa=empresa,
                direccion=direccion
            )

            db.session.add(proveedor)
            db.session.commit()

            return {"mensaje" : "Proveedor creado"}
        
        except:
            return {"error" : "No pudo crearse el proveedor"}
    
    def get_proveedores(self):
        return Proveedor.query.all()
    
    def get_proveedor(self, id):
        proveedor = Proveedor.query.get(id)

        if proveedor is None:
            return None
        
        return proveedor
    
    def get_proovedor_cod_proveedor(self, cod_proveedor):
        return Proveedor.query.filter_by(cod_proveedor=cod_proveedor).first()

    def update_proveedor(self, id):
        proveedor = Proveedor.query.get(id)

        if proveedor is None:
            return None
        
        if 'nombre' in request.json: proveedor.nombre = request.json['nombre']
        if 'telefono' in request.json: proveedor.telefono = request.json['telefono']
        if 'empresa' in request.json: proveedor.empresa = request.json['empresa']
        if 'direccion' in request.json: proveedor.direccion = request.json['direccion']
        if 'cod_proveedor' in request.json: 
            cod_proveedor = request.json['cod_proveedor']
            proveedor.cod_proveedor = cod_proveedor.upper()

        db.session.commit()

        return proveedor
    
    def delete_proveedor(self, id):
        proveedor = Proveedor.query.get(id)

        if proveedor is None:
            return None
        try:
            db.session.delete(proveedor)
            db.session.commit()

            return {"mensaje" : "Proveedor eliminado"}
        
        except:
            return {"error" : "Proveedor no se pudo eliminar, algo salio mal"}