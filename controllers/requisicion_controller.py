from app import db
from flask import request
from models.requisicion.requisicion import Requisicion

class RequisicionController():

    def create_requisicion(self):
        request_data = request.get_json()
        requisicion = Requisicion(**request_data)

        db.session.add(requisicion)
        db.session.commit()

        return requisicion
    
    def get_requisiciones(self):
        return Requisicion.query.all()
    
    def get_requisicion(self, id):
        requisicion = Requisicion.query.get(id)

        if requisicion is None: return None

        return requisicion

    def update_requisicion(self, id):
        requisicion = Requisicion.query.get(id)

        if requisicion is None: return None

        if 'fecha_entrega_requerida' in request.json : requisicion.fecha_entrega_requerida = request.json['fecha_entrega_requerida']
        if 'descripcion' in request.json : requisicion.descripcion = request.json['descripcion']
        if 'estado' in request.json : requisicion.estado = request.json['estado']
        if 'proyecto_id' in request.json : requisicion.proyecto = request.json['proyecto_id']
        if 'costo' in request.json: requisicion.costo = request.json['costo']

        db.session.commit()

        return requisicion
    
    def delete_requisicion(self, id):
        requisicion = Requisicion.query.get(id)    

        if requisicion is None: return None

        db.session.delete(requisicion)
        db.session.commit()

        return requisicion
    