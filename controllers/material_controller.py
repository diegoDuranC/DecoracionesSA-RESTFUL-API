from models.material.material import Material
from app import db
from flask import request


class MaterialController():

    def create_material(self):
        request_data = request.get_json()
        material = Material(**request_data)
        db.session.add(material)
        db.session.commit()

        return material
    
    def get_material(self, material_id):
        material = Material.query.get(material_id)
        return material

    def get_materiales(self):
        return db.session.query(Material).all()

    def update_material(self, material_id):
        material = Material.query.get(material_id)

        if material is None:
            return None #Manejar un error de que no existe dicho objeto en la BD
        
        if 'descripcion' in request.json:
            material.descripcion = request.json['descripcion']
            
        if 'existencias' in request.json:
            material.existencias = request.json['existencias']

        db.session.commit()

        return material
    
    def delete_material(self, material_id):
        material = Material.query.get(material_id)

        if material is None:
            return None
        
        db.session.delete(material)
        db.session.commit()

        return material
