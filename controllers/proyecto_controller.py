from models.proyecto import Proyecto
from models.cliente.cliente import Cliente
from models.rrhh.empleado import Empleado, EmpleadoSchema
from models.rrhh.cargo import Cargo
from sqlalchemy.exc import SQLAlchemyError
from models.proyecto import ProyectoSchema
from app import db
from flask import request

proyecto_schema = ProyectoSchema()
proyecto_schemas = ProyectoSchema(many=True)

class ProyectoController():

    def create_proyecto(self):
        #empleado_schema = EmpleadoSchema()

        cod_proyecto = request.json.get('cod_proyecto')
        nombre_proyecto = request.json.get('nombre_proyecto')
        descripcion_proyecto = request.json.get('descripcion_proyecto') 
        #encargado_proyecto_id = request.json.get('encargado_proyecto_id')
        #cliente_id = request.json.get('cliente_proyecto_id')
        codigo_cliente = request.json.get('cod_cliente')
        codigo_coordinador = request.json.get('cod_empleado')
        ''' 
            campos necesarios
            codigo_cliente
            codigo_coordinador
        '''

        cliente = Cliente.query.filter_by(cod_cliente=codigo_cliente).first()

        if not cliente :
            return {"Error" : "Cliente no encontrado"}
        
        encargado = Empleado.query.filter_by(cod_empleado=codigo_coordinador).first()

        if not encargado:
            return {"Error" : "Encargado no encontrado"}
        
        print(cliente)
        print(encargado)
    
        # Verificar si el cargo del encargado es ARQUITECTO
        if encargado.cargo.cargo != 'ARQUITECTO':
            return {"Error": "El encargado debe ser un arquitecto"}
        
        if encargado.cargo.cargo == 'ARQUITECTO':

            proyecto = Proyecto(
                cod_proyecto=cod_proyecto,
                nombre_proyecto=nombre_proyecto,
                descripcion_proyecto=descripcion_proyecto,
                encargado_proyecto_id=encargado.ID_empleado,
                cliente_id=cliente.ID_cliente
            )

            try:
                db.session.add(proyecto)
                db.session.commit()

                return True
        
            except SQLAlchemyError as e:
                db.session.rollback()
                return {"Error": str(e)}
            
        else:
            return {"Error" : "Ingrese un arquitecto"}
    
    def get_proyectos(self):
        proyectos = Proyecto.query.all()
        return proyecto_schemas.dump(proyectos)
    
    def get_proyecto(self, id):
        proyecto = Proyecto.query.get(id)

        if proyecto is None:
            return None
        
        return proyecto_schema.dump(proyecto)
    
    def update_proyecto(self, id):
        proyecto = Proyecto.query.get(id)
        if proyecto is None:
            return None

        if 'cod_proyecto' in request.json: proyecto.cod_proyecto = request.json['cod_proyecto']
        if 'nombre_proyecto' in request.json: proyecto.nombre_proyecto = request.json['nombre_proyecto']
        if 'descripcion_proyecto' in request.json: proyecto.descripcion_proyecto = request.json['descripcion_proyecto']
        if 'cod_cliente' in request.json: 
            cod_cliente = request.json['cod_cliente']
            cliente = Cliente.query.filter_by(cod_cliente=cod_cliente).first()

            if not cliente :
                return {"Error" : "Cliente no encontrado"}

            proyecto.cliente_id = cliente.ID_cliente

        if 'cod_empleado' in request.json:
            cod_encargado = request.json.get('cod_empleado')

            encargado = Empleado.query.filter_by(cod_empleado=cod_encargado).first()

            if not encargado:
                return {"Error" : "Encargado no encontrado"}
            
            if encargado.cargo.cargo != 'ARQUITECTO':
                return {"Error": "El encargado debe ser un arquitecto"}

            proyecto.encargado_proyecto_id = encargado.ID_empleado


        db.session.commit()
        return proyecto_schema.dump(proyecto)
    
    def delete_proyecto(self, id):
        proyecto = Proyecto.query.get(id)

        if proyecto is None:
            return None
        
        try:
            db.session.delete(proyecto)
            db.session.commit()

            return True
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"Error": str(e)}
        