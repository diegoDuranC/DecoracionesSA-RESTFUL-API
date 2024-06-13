from models.rrhh.departamento import Departamento, DepartamentoSchema
from app import db
from flask import request

departamento_schema = DepartamentoSchema()
departamento_schemas = DepartamentoSchema(many=True)

class DepartamentoController():

    def create_departamento(self):
            nombre_departamento = request.json['departamento']
    
            if nombre_departamento == "" :
                return {"Error" : "Se necesita el nombre del departamento"}
            
            nombre_departamento = nombre_departamento.upper()

            nuevo_departamento = Departamento(nombre_departamento)

            db.session.add(nuevo_departamento)
            db.session.commit()

            return departamento_schema.dump(nuevo_departamento)
    
    def get_departamentos(self):
        departamentos = Departamento.query.all()

        if not departamentos:
             return {"Error" : "No hay departamentos"}

        return departamento_schemas.dump(departamentos)
    
    def get_departamento(self, ID_departamento):
        departamento = Departamento.query.get(ID_departamento)

        if not departamento:
             return {"Error" : "Departamento no encontrado"}

        return departamento_schema.dump(departamento)

    def update_departamento(self, ID_departamento):
        departamento = Departamento.query.get(ID_departamento)

        if 'departamento' in request.json:
            departamento = request.json['departamento']
            departamento.departamento = departamento.upper()
        
        else:
             return {"Error" : "Falta el campo 'departamento'"}

        return departamento_schema.dump(departamento)
    
    def delete_departamento(self, ID_departamento):
         departamento = Departamento.query.get(ID_departamento)

         if not departamento:
             return {"Error" : "Departamento no encontrado"}

         db.session.delete(departamento)
         db.session.commit()

         return departamento_schema.dump(departamento)
