from models.material.material import Material
from sqlalchemy.exc import SQLAlchemyError
from app import db
from flask import request


class MaterialController():

    def create_material(self):
        
        cod_material = request.json.get('cod_material')
        descripcion = request.json.get('descripcion')
        existencias = request.json.get('existencias')
        precio_unitario = request.json.get('precio_unitario')

        material = Material(
            cod_material=cod_material, descripcion=descripcion, existencias= existencias, precio_unitario=precio_unitario
        )
        
        try:
            db.session.add(material)
            db.session.commit()

            return True
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"Error": str(e)}
    
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

        if 'cod_material' in request.json:
            material.cod_material = request.json['cod_material']

        if 'precio_unitario' in request.json:
            material.precio_unitario = request.json['precio_unitario']

        db.session.commit()

        return material
    
    def delete_material(self, material_id):
        material = Material.query.get(material_id)

        if material is None:
            return None
        
        db.session.delete(material)
        db.session.commit()

        return material
