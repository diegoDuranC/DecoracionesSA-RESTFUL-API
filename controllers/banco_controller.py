from models.banco import Banco
from app import db
from flask import request

class BancoController():

    def create_banco(self):
        request_data = request.get_json()
        banco = Banco(**request_data)
        db.session.add(banco)
        db.session.commit()
        
        return banco
    
    def get_bancos(self):
        return Banco.query.all()
    
    def get_banco(self, id):
        banco = Banco.query.get(id)
        return banco
    
    def update_banco(self, id):
        banco = Banco.query.get(id)

        if banco is None:
            return None #Manejar un error de que no existe dicho objeto en la BD
        
        if 'nombre' in request.json:
            banco.nombre = request.json['nombre']
        if 'ciudad' in request.json:
            banco.ciudad = request.json['ciudad']
        if 'direccion' in request.json:
            banco.direccion = request.json['direccion']

        db.session.commit()

        return banco
    
    def delete_banco(self, id):
        banco = Banco.query.get(id)

        if banco is None:
            return None
        
        db.session.delete(banco)
        db.session.commit()

        return banco