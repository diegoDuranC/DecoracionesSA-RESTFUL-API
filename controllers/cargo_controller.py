from models.rrhh.cargo import Cargo
from app import db
from flask import request

class CargoController():
    
    def create_cargo(self):
        cargo = request.json['cargo']
        cod_cargo = request.json['cod_cargo']

        upper_cargo = cargo.upper()
        upper_cod_cargo = cod_cargo.upper()

        if cargo is None:
            return None
        
        nuevo_cargo = Cargo(cargo=upper_cargo, cod_cargo=upper_cod_cargo)

        db.session.add(nuevo_cargo)
        db.session.commit()

        return nuevo_cargo
    
    def get_cargo(self, cargo_id):
        cargo = Cargo.query.get(cargo_id)
        return cargo

    def get_cargos(self):
        return Cargo.query.all()

    def update_cargo(self, cargo_id):
        cargo = Cargo.query.get(cargo_id)

        if cargo is None:
            return None #Manejar un error de que no existe dicho objeto en la BD
        
        if 'cargo' in request.json:
            upper_cargo = request.json['cargo']
            cargo.cargo = upper_cargo.upper()

        if 'cod_cargo' in request.json:
            upper_cod_cargo = request.json['cod_cargo']
            cargo.cod_cargo = upper_cod_cargo.upper()

        db.session.commit()

        return cargo
    
    def delete_cargo(self, cargo_id):
        cargo = Cargo.query.get(cargo_id)

        if cargo is None:
            return None
        try:
            db.session.delete(cargo)
            db.session.commit()

            return {"Mensaje" : "Cargo eliminado"}
    
        except:
            return {"Error" : "No se pudo eliminar"}
        
    def get_cargo_cod(self, cod_cargo):
        codigo_cargo = cod_cargo.upper()
        cargo = Cargo.query.filter_by(cod_cargo=codigo_cargo).first()

        if cargo is None:
            return None
        
        return cargo

        