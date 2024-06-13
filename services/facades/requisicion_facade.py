from re import T
from models.requisicion.requisicion import Requisicion, RequisicionSchema
from models.requisicion.detalle_materiales import DetalleMaterialRequisicion
from models.material.material import Material
from models.material.transacciones_inventario import TransaccionInventario
from models.proyecto import Proyecto
from sqlalchemy.exc import IntegrityError
from models.requisicion.requisicion import RequisicionSchema

from app import db

requisicion_schema = RequisicionSchema()
requisicion_schemas = RequisicionSchema(many=True)

class RequisicionFacade():
    

    def get_requisiciones(self):

      consulta = Requisicion.query.all()

      if not consulta:
        return {"Mensaje" : "No hay requisiciones"}
      
      requisicion_schemas = RequisicionSchema(many=True)      
      result = requisicion_schemas.dump(consulta)

      return result
    
    def get_requisicion_proyecto(self, nro_proyecto):
        consulta = Requisicion.query.filter_by(proyecto_id=nro_proyecto).all()

        if not consulta:
            return {"Mensaje" : "No hay requisicion"}
    
        return consulta
    
    def get_requisicion(self, nro_requisicion):

        requisicion = Requisicion.query.get(nro_requisicion)

        if requisicion: return requisicion
            # requisicion_schema = RequisicionSchema()
            # result = requisicion_schema.dump(requisicion)
            # return result
        else:
            return None
        
    def crear_requisicion(self, request_data):
        try:
            # Datos para requisicion - ENCABEZADO
            fecha_entrega_requerida = request_data.get('fecha_entrega_requerida')
            descripcion = request_data.get('descripcion')
            costo = request_data.get('costo')
            proyecto_id = request_data.get('proyecto_nro_proyecto')
            materiales = request_data.get('materiales_solicitados')

            # CREAR LA REQUISICION
            requisicion = Requisicion(
                fecha_entrega_requerida=fecha_entrega_requerida,
                descripcion=descripcion,
                costo=costo,
                proyecto_nro_proyecto=proyecto_id
            )

            db.session.add(requisicion)
            db.session.commit()
            
            print("Requisicion creada:", requisicion.nro_requisicion)

            # Crear DetalleMaterialRequisicion para cada material solicitado
            for item in materiales:
                id_material = item.get('id_material')
                cantidad_solicitada = item.get('cantidad_solicitada')

                # VERIFICAR EXISTENCIAS
                material = Material.query.get(id_material)

                if material.existencias < cantidad_solicitada:
                    raise Exception(f"¡No hay suficiente stock disponible de {material.descripcion}!")

                material.existencias -= cantidad_solicitada
                db.session.commit()

                print("Existencias actualizadas para material:", material.ID_material)

                detalle_material = DetalleMaterialRequisicion(
                    id_material=id_material,
                    cantidad_solicitada=cantidad_solicitada,
                    nro_requisicion=requisicion.nro_requisicion
                )
                db.session.add(detalle_material)
                db.session.commit()

                print("DetalleMaterialRequisicion creado:", detalle_material.ID)

                # Crear transacción de inventario
                codigo_transaccion = f"{detalle_material.ID}-S"
                nueva_transaccion = TransaccionInventario(
                    codigo_transaccion=codigo_transaccion,
                    id_material=id_material,
                    descripcion=material.descripcion,
                    precio_unitario=material.precio_unitario,
                    fecha_transaccion=requisicion.fecha_creacion,
                    cantidad_entrada=0,
                    cantidad_salida=cantidad_solicitada,
                    existencia_salida=material.existencias,
                    detalle_material_id=detalle_material.ID,
                    material_recibido_id=None
                )
                db.session.add(nueva_transaccion)

                db.session.commit()
                print("TransaccionInventario creada:", nueva_transaccion.id)

            return True
    
        except IntegrityError as e:
            db.session.rollback()
            return {'error': 'Error de base de datos al crear la requisición'}
        
    def agregar_detalle_a_requisicion(self, nro_requisicion, materiales):
        requisicion = Requisicion.query.get(nro_requisicion)

        if not requisicion:
            return {'error': 'Requisición no encontrada'}, 404
        
        try:
            for material in materiales:
                # Verificar si el detalle ya existe
                detalle_existente = DetalleMaterialRequisicion.query.filter_by(nro_requisicion=nro_requisicion, id_material=material['id_material']).first()

                if detalle_existente:
                    return {'error': f'Detalle con ID de material {material["id_material"]} ya existe en la requisición'}
                
                nuevo_detalle = DetalleMaterialRequisicion(
                    id_material=material['id_material'],
                    cantidad_solicitada=material['cantidad_solicitada'],
                    nro_requisicion=nro_requisicion
                )
                db.session.add(nuevo_detalle)

                # Actualizar existencias de material
                material_obj = Material.query.get(material['id_material'])

                if material_obj:
                    material_obj.existencias -= material['cantidad_solicitada']
                    if material_obj.existencias < 0:
                        raise Exception(f"No hay suficiente stock disponible de {material_obj.descripcion}!")
                    db.session.commit()

                else:
                    return {'error': f'Material con ID {material["id_material"]} no encontrado'}

                # Crear una nueva transacción de inventario
                codigo_transaccion = f"{nuevo_detalle.ID}-S"

                nueva_transaccion = TransaccionInventario(
                    detalle_material_id=nuevo_detalle.ID,
                    cantidad_salida=material['cantidad_solicitada'],
                    existencia_salida=material_obj.existencias,
                    codigo_transaccion=codigo_transaccion,
                    id_material=material['id_material'],
                    descripcion=material_obj.descripcion,
                    precio_unitario=material_obj.precio_unitario,
                    fecha_transaccion=requisicion.fecha_creacion,
                    cantidad_entrada=0,
                    material_recibido_id=None
                )

                db.session.add(nueva_transaccion)
                db.session.commit()

            return {'Mensaje': 'Detalles de requisición agregados exitosamente'}

        except IntegrityError as e:
            db.session.rollback()
            return {'error': 'Error de base de datos al agregar los detalles a la requisición'}
        
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}
    
    def eliminar_requisicion(self, nro_requisicion):
        requisicion = Requisicion.query.get(nro_requisicion)

        if not requisicion:
            return None

        # Revertir cambios en los materiales solicitados
        materiales_solicitados = requisicion.materiales_solicitados
        for detalle_material in materiales_solicitados:
            material_id = detalle_material.id_material
            material = Material.query.get(material_id)
            if material:
                material.existencias += detalle_material.cantidad_solicitada

                # Eliminar la transacción de inventario asociada al detalle_material
                transaccion = TransaccionInventario.query.filter_by(detalle_material_id=detalle_material.ID).first()
                if transaccion:
                    db.session.delete(transaccion)

            # Eliminar la transacción de inventario asociada al detalle_material
            transaccion = TransaccionInventario.query.filter_by(detalle_material_id=detalle_material.ID).first()
            if transaccion:
                db.session.delete(transaccion)

        # Eliminar los detalles de materiales solicitados de la requisición
        db.session.delete(requisicion)

        db.session.commit()

        return {'Mensaje': 'Requisición eliminada exitosamente'}
    
    def actualizar_encabezado_requisicion(self, nro_requisicion, request_data):

        requisicion = Requisicion.query.get(nro_requisicion)

        if not requisicion: return {"Error" : "La requisicion no existe"}

        if 'fecha_entrega_requerida' in request_data:
            requisicion.fecha_entrega_requerida = request_data['fecha_entrega_requerida']
        if 'descripcion' in request_data:
            requisicion.descripcion = request_data['descripcion']
        if 'costo' in request_data:
            requisicion.costo = request_data['costo']
        if 'proyecto_nro_proyecto' in request_data:
            requisicion.proyecto_nro_proyecto = request_data['proyecto_nro_proyecto']

        db.session.commit()

        return {"Mensaje" : "Requisicion actualizada"}


    def actualizar_detalles_requisicion(self, nro_requisicion, request_data):

        requisicion = Requisicion.query.get(nro_requisicion)
    
        if not requisicion:
            return {'error': 'Requisición no encontrada'}, 404
        
        try:

            for detalle_nuevo in request_data['materiales_solicitados']:
                detalle_actual = next((detalle for detalle in requisicion.materiales_solicitados if detalle.ID == detalle_nuevo['ID']), None)
                
                if detalle_actual:
                    cantidad_anterior = detalle_actual.cantidad_solicitada
                    cantidad_nueva = detalle_nuevo['cantidad_solicitada']
                    diferencia_cantidad = cantidad_nueva - cantidad_anterior

                    # Actualizar cantidad solicitada en el detalle
                    detalle_actual.cantidad_solicitada = cantidad_nueva

                    # Actualizar existencias de material
                    material = Material.query.get(detalle_actual.id_material)

                    if material:
                        material.existencias -= diferencia_cantidad  # Restar la diferencia

                        if material.existencias < 0:
                            raise Exception(f"No hay suficiente stock disponible de {material.descripcion}!")
                        db.session.commit()

                    else:
                        return {'error': f'Material con ID {detalle_actual.id_material} no encontrado'}

                    # Actualizar transacción de inventario
                    transaccion = TransaccionInventario.query.filter_by(detalle_material_id=detalle_actual.ID).first()

                    if transaccion:
                        transaccion.cantidad_salida += diferencia_cantidad  # Ajustar la cantidad de salida
                        transaccion.existencia_salida -= diferencia_cantidad  # Restar la diferencia
                        db.session.commit()

                    else:
                        return {'error': f'Transacción de inventario para detalle de material con ID {detalle_actual.ID} no encontrada'}
                else:
                    return {'error': f'Detalle de material con ID {detalle_nuevo["ID"]} no encontrado'}

            return {'Mensaje': 'Detalles de requisición actualizados exitosamente'}

        except IntegrityError as e:
            db.session.rollback()
            return {'error': 'Error de base de datos al actualizar los detalles de la requisición'}
        
    def eliminar_detalle_requisicion(self, nro_requisicion, id_detalle):
        requisicion = Requisicion.query.get(nro_requisicion)

        if not requisicion:
            return {"Error": "La requisición no existe"}

        # Buscar el detalle de requisición a eliminar
        detalle_a_eliminar = next((detalle for detalle in requisicion.materiales_solicitados if detalle.ID == id_detalle), None)

        if not detalle_a_eliminar:
            return {"Error": f"No se encontró el detalle de requisición con ID {id_detalle}"}

        # Eliminar la transacción de inventario asociada al detalle de requisición
        transaccion = TransaccionInventario.query.filter_by(detalle_material_id=detalle_a_eliminar.ID).first()

        if transaccion:
            db.session.delete(transaccion)

        # Aumentar las existencias del material asociado al detalle de requisición eliminado
        material = Material.query.get(detalle_a_eliminar.id_material)

        if material:
            material.existencias += detalle_a_eliminar.cantidad_solicitada

        # Eliminar el detalle de requisición
        db.session.delete(detalle_a_eliminar)

        # Guardar los cambios en la base de datos
        db.session.commit()

        return {"Mensaje": "Detalle de requisición eliminado exitosamente"}