from models.proyecto import Proyecto
from app import db
from flask import request

class ProyectoController():

    def create_proyecto(self):
        request_data = request.get_json()
        proyecto = Proyecto(**request_data)
        
        db.session.add(proyecto)
        db.session.commit()

        return proyecto
    
    def get_proyectos(self):
        return Proyecto.query.all()
    
    def get_proyecto(self, id):
        proyecto = Proyecto.query.get(id)

        if proyecto is None:
            return None
        
        return proyecto
    
    def update_proyecto(self, id):
        proyecto = Proyecto.query.get(id)

        if proyecto is None:
            return None
        
        if 'numero_proyecto' in request.json: proyecto.numero_proyecto = request.json['numero_proyecto']
        if 'nombre_proyecto' in request.json: proyecto.nombre_proyecto = request.json['nombre_proyecto']
        if 'descripcion_proyecto' in request.json: proyecto.descripcion_proyecto = request.json['descripcion_proyecto']
        if 'cliente_id' in request.json: proyecto.cliente_id = request.json['cliente_id']
        if 'encargado_proyecto' in request.json: proyecto.encargado_proyecto = request.json['encargado_proyecto']

        db.session.commit()

        return proyecto
    
    def delete_proyecto(self, id):
        proyecto = Proyecto.query.get(id)

        if proyecto is None:
            return None
        
        db.session.delete(proyecto)
        db.session.commit()

        return proyecto
        