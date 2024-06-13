from models.rrhh.departamento import Departamento
from models.rrhh.empleado import Empleado, EmpleadoSchema
from sqlalchemy.exc import SQLAlchemyError
from app import db
from flask import request

empleado_schema = EmpleadoSchema()
empleado_schemas = EmpleadoSchema(many=True)

class EmpleadoController():

    def create_empleado(self):
        try:
            request_data = request.get_json()
            #departamento = Departamento.query.get(request_data.get('departamento_id'))

            #FORMATEANDO EL CODIGO DEL EMPLEADO
            #codigo_empleado = departamento.departamento[:3] + "-" + request_data.get('ci') + request_data.get('nombre')[:1] + request_data.get('apellido')[:1]
            
            empleado = Empleado(
                cod_empleado = request_data.get('cod_empleado'),
                ci = request_data.get('ci'), 
                nombre = request_data.get('nombre'),
                apellido = request_data.get('apellido'),
                telefono = request_data.get('telefono'),
                cargo_id = request_data.get('cargo_id'),
                departamento_id = request_data.get('departamento_id'),
            )
            
            db.session.add(empleado)
            db.session.commit()

            return True
        
        except SQLAlchemyError as e:
                db.session.rollback()
                return {"Error": str(e)}
    
    def get_empleado(self, id_empleado):
        empleado = Empleado.query.get(id_empleado)
        return empleado_schema.dump(empleado)
    
    def get_empleados(self):
        empleados = Empleado.query.all()
        return empleado_schemas.dump(empleados)
    
    def get_empleado_ci(self, ci):
        empleado = Empleado.query.filter_by(ci=ci).first()
        return empleado_schema.dump(empleado)
    
    def update_empleado(self, ID_empleado):
        empleado = Empleado.query.get(ID_empleado)

        if not empleado :
            return {"Error" : "No se encuentra el empleado"}

        if 'ci' in request.json : empleado.ci = request.json['ci']

        if 'nombre' in request.json : 
            nombre = request.json['nombre']
            empleado.nombre = nombre.upper()

        if 'apellido' in request.json : 
            apellido = request.json['apellido']
            empleado.apellido = apellido.upper()

        if 'telefono' in request.json : empleado.telefono = request.json['telefono']

        if 'cargo_id' in request.json : 
            cargo = request.json['cargo_id']
            empleado.cargo_id = cargo
        
        if 'departamento_id' in request.json : empleado.departamento_id = request.json['departamento_id']

        if 'cod_empleado' in request.json : 
            cod_empleado = request.json['cod_empleado']
            empleado.cod_empleado = cod_empleado.upper()
    
        db.session.commit()

        return empleado_schema.dump(empleado)

    
    def delete_empleado(self, ID_empleado):
        empleado = Empleado.query.get(ID_empleado)

        if not empleado:
            return {"Error": "Empleado no encontrado"}
        
        if empleado.proyectos:  # Verifica si el empleado tiene proyectos asignados
            return {"error": "No se puede eliminar al empleado, pertenece a un proyecto"}
        
        db.session.delete(empleado)
        db.session.commit()

        return True