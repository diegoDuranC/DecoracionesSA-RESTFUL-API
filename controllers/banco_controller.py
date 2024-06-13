from models.banco.banco import Banco
from app import db
from flask import request
from models.banco.banco import BancoSchema

banco_schema = BancoSchema()
banco_schemas = BancoSchema(many=True)

class BancoController():

    def create_banco(self,request_data):
        try:       
            cod_banco = request_data.get('cod_banco')
            nombre = request_data.get('nombre')
            direccion = request_data.get('direccion')
            ciudad = request_data.get('ciudad')

            cod_ban = cod_banco.upper()

            banco = Banco(
                cod_banco=cod_ban,
                nombre=nombre,
                direccion=direccion,
                ciudad=ciudad
            )

            db.session.add(banco)
            db.session.commit()
            
            return {"mensaje" : "Banco creado"}
        except:
            return {"error" : "Banco no creado, algo salió mal"}
        
    def get_bancos(self):
        return Banco.query.all()
    
    def get_banco(self, id):
        banco = Banco.query.get(id)
        
        if banco is None: return None

        return banco
    
    def get_banco_cod_banco(self, cod_banco):
        bancos = Banco.query.filter(Banco.cod_banco.like(f"%{cod_banco}%")).all()

        if not bancos:
            return {"mensaje" : "Banco no encontrado"}
        
        return banco_schemas.dump(bancos)
    
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
        if 'cod_banco' in request.json:
            cod_ban = request.json['cod_banco']
            banco.cod_banco = cod_ban.upper()

        db.session.commit()

        return banco
    
    def delete_banco(self, id):
        banco = Banco.query.get(id)

        if banco is None:
            return None
        
        db.session.delete(banco)
        db.session.commit()

        return banco