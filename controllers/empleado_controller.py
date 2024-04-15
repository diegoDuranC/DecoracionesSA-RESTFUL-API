from models.empleado import Empleado
from app import db
from flask import request

class EmpleadoController():

    def create_empleado(self):
        request_data = request.get_json()
        empleado = Empleado(**request_data)
        
        db.session.add(empleado)
        db.session.commit()

        return empleado
    
    def update_empleado(self, id_empleado):
        empleado = Empleado.query.get(id_empleado)

        if empleado is None:
            return None #Manejar un error de que no existe dicho objeto en la BD

        if 'ci_empleado' in request.json:
            empleado.ci_empleado = request.json['ci_empleado']

        if 'nombre_empleado' in request.json:
            empleado.nombre_empleado = request.json['nombre_empleado']

        if 'apellido_empleado' in request.json:
            empleado.apellido_empleado = request.json['apellido_empleado']

        if 'telefono_empleado' in request.json:
            empleado.telefono_empleado = request.json['telefono_empleado']

        if 'cargo' in request.json:
            empleado.cargo = request.json['cargo'] 
        
        if 'area' in request.json:
            empleado.area = request.json['area']
        
        if 'jefe_id' in request.json:
            empleado.jefe_id = request.json['jefe_id']
        
        if 'estado' in request.json:
            empleado.estado = request.json['estado'].upper()

        if 'fecha_contratacion' in request.json:
            empleado.fecha_contracion = request.json['fecha_contracion']
        
        if 'fecha_despido' in request.json:
            empleado.fecha_despido = request.json['fecha_despido']
        
        db.session.commit()

        return empleado

    def get_empleado(self, id_empleado):
        empleado = Empleado.query.get(id_empleado)
        return empleado
    
    def get_empleados(self):
        return Empleado.query.all()
    