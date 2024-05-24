from models.rrhh.cargo import Cargo
from app import db
from flask import request

class CargoController():
    
    def create_cargo(self):
        cargo = request.json['cargo']

        if cargo is None:
            return None
        
        nuevo_cargo = Cargo(cargo)

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
            cargo.cargo = request.json['cargo']

        db.session.commit()

        return cargo
    
    def delete_cargo(self, cargo_id):
        cargo = Cargo.query.get(cargo_id)

        if cargo is None:
            return None
        
        db.session.delete(cargo)
        db.session.commit()

        return cargo