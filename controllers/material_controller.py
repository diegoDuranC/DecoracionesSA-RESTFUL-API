from models.material import Material
from app import db
from flask import request


class MaterialController():

    def create_material(self):
        request_data = request.get_json()
        material = Material(**request_data)
        db.session.add(material)
        db.session.commit()

        return material
    
    # def create_materiales(self):
    #     materiales = request.json()

    #     for material in materiales:

    #         descripcion = material['descripcion']
    #         precio_unitario = material['precio_unitario']
    #         existencias = material['existencias']

    #         new_material = Material(descripcion, precio_unitario, existencias)
    #         db.session.add(new_material)
        
    #     db.session.commit()

    #     return materiales
    
    def get_material(self, material_id):
        material = Material.query.get(material_id)
        return material

    def get_materiales(self):
        return Material.query.all()

    def update_material(self, material_id):
        material = Material.query.get(material_id)

        if material is None:
            return None #Manejar un error de que no existe dicho objeto en la BD
        
        if 'descripcion' in request.json:
            material.descripcion = request.json['descripcion']
        if 'precio_unitario' in request.json:
            material.precio_unitario = request.json['precio_unitario']
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
