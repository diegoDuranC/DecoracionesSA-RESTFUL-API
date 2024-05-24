from models.requisicion.requisicion import Requisicion, RequisicionSchema
from models.requisicion.detalle_materiales import DetalleMaterialRequisicion
from models.material.material import Material
from models.proyecto import Proyecto
from sqlalchemy.exc import IntegrityError


from app import db
from flask import jsonify

class RequisicionFacade():
    
    def crear_requisicion(self, request_data):
        try:
            #Datos para requisicion - ENCABEZADO
            fecha_entrega_requerida = request_data.get('fecha_entrega_requerida')
            descripcion = request_data.get('descripcion')
            costo = request_data.get('costo')
            proyecto_id = request_data.get('proyecto_id')
            materiales = request_data.get('materiales')

            #CREAR LA REQUISICION
            requisicion = Requisicion(
                fecha_entrega_requerida=fecha_entrega_requerida,
                descripcion=descripcion,
                costo=costo,
                proyecto_id=proyecto_id
            )

            db.session.add(requisicion)
            db.session.commit()

            # Crear DetalleMaterialRequisicion para cada material solicitado

            for item in materiales:
                codigo_material = item.get('codigo_material')
                cantidad_solicitada = item.get('cantidad_solicitada')

                #VERIFICAR EXISTENCIAS

                material = Material.query.get(codigo_material)

                if material.existencias < cantidad_solicitada:
                    raise Exception(f"¡No hay suficiente stock disponible de {material.descripcion}!")

                material.existencias -= cantidad_solicitada
                db.session.commit()

                detalle_material = DetalleMaterialRequisicion(
                    codigo_material=codigo_material,
                    cantidad_solicitada=cantidad_solicitada,
                    nro_requisicion=requisicion.nro_requisicion
                )
                db.session.add(detalle_material)

            db.session.commit()

            return requisicion
    
        except IntegrityError as e:
            # Manejar la excepción de integridad de la base de datos (por ejemplo, violación de una restricción única)
            db.session.rollback()
            # Registro de errores
            # Devolver un mensaje de error significativo
            return jsonify({'error': 'Error de base de datos al crear la requisición'}), 500
        
    def get_requisiciones(self):

      consulta = Requisicion.query.join(Requisicion.proyecto).join(Proyecto.cliente).all()

      requisicion_schemas = RequisicionSchema(many=True)
      result = requisicion_schemas.dump(consulta)

      return result
    
    def get_requisicion_proyecto(self, nro_proyecto):
        consulta = Requisicion.query.filter_by(proyecto_id=nro_proyecto).all()
        return consulta
    
    def get_requisicion(self, nro_requisicion):

        #requisicion = Requisicion.query.filter_by(nro_requisicion=nro_requisicion).first()
        requisicion = Requisicion.query.get(nro_requisicion)

        if requisicion: return requisicion
            # requisicion_schema = RequisicionSchema()
            # result = requisicion_schema.dump(requisicion)
            # return result
        else:
            return None