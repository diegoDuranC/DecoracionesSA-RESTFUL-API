from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app import db
from models.material.material import Material
from models.compras.orden_de_compra import OrdenDeCompra, OrdenDeCompraSchema, EstadoCompra
from models.compras.detalle_orden import DetalleOrdenCompra, DetalleOrdenCompraSchema

class OrdenDeCompraFacade:

    def __init__(self):
        self.orden_schema = OrdenDeCompraSchema()
        self.detalle_schema = DetalleOrdenCompraSchema()

    def crear_orden_de_compra(self, descripcion, cod_orden, materiales):
        """
        Crea una orden de compra con los materiales requeridos.
        
        :param descripcion: Descripción de la orden de compra.
        :param materiales: Lista de materiales y sus cantidades requeridas. 
                           Formato: [{'codigo_material': 1, 'cantidad_requerida': 10, 'precio_material': 50.00}, ...]
        :return: La orden de compra creada.
        """
        try:
            # Crear la orden de compra
            nueva_orden = OrdenDeCompra(
                descripcion=descripcion,
                cod_orden=cod_orden,
                estado_compra=EstadoCompra.PENDIENTE
            )

            db.session.add(nueva_orden)
            db.session.flush()  # Asegura que se genere el nro_orden
            
            # Crear los detalles de la orden de compra
            for material_data in materiales:
                id_material = material_data.get('ID_material')
                cantidad_requerida = material_data.get('cantidad_requerida')
                precio_material = material_data.get('precio_material')
                
                material = Material.query.get(id_material)
                if not material:
                    return {"error": f"Material con código {id_material} no encontrado"}

                detalle = DetalleOrdenCompra(
                    cantidad_requerida=cantidad_requerida,
                    precio_material=precio_material,
                    id_material=id_material,
                    nro_orden=nueva_orden.nro_orden
                )
                db.session.add(detalle)
            
            db.session.commit()
            return self.orden_schema.dump(nueva_orden)
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}
        
    def obtener_orden_por_id(self, nro_orden):
        """
        Obtiene una orden de compra por su número de orden.
        
        :param nro_orden: Número de la orden de compra.
        :return: La orden de compra y sus detalles.
        """
        orden = OrdenDeCompra.query.get(nro_orden)
        if not orden:
            return {"error": "Orden de compra no encontrada"}
        
        detalles = DetalleOrdenCompra.query.filter_by(nro_orden=nro_orden).all()
        return {
            "orden": self.orden_schema.dump(orden)
        }

    def obtener_todas_las_ordenes(self):
        """
        Obtiene todas las órdenes de compra.
        
        :return: Lista de todas las órdenes de compra.
        """
        ordenes = OrdenDeCompra.query.all()

        if not ordenes:
            return {"error" : "no hay ordenes"}
        return self.orden_schema.dump(ordenes, many=True)
    
    def obtener_ordenes_pendientes(self):
        """
            Obtiene todas las ordenes pendientes es decir que no se ha recibido ni un solo material
        """
        ordenes = OrdenDeCompra.query.filter_by(estado_compra=EstadoCompra.PENDIENTE).all()

        if not ordenes:
            return {"mensaje" : "no hay ordenes pendientes"}
        
        return self.orden_schema.dump(ordenes, many=True)

    def obtener_ordenes_parcialmente_satisfechas(self):
        """
            Obtiene todas las ordenes de las cuales se han recibido al menos un material
        """
        ordenes = OrdenDeCompra.query.filter_by(estado_compra=EstadoCompra.PARCIALMENTE_SATISFECHA).all()

        if not ordenes:
            return {"mensaje" : "no hay ordenes parcialmente satisfechas"}
        
        return self.orden_schema.dump(ordenes, many=True)
    
    def obtener_ordenes_satisfechas(self):
        """
            Obtiene las ordenes satisfechas
        """
        ordenes = OrdenDeCompra.query.filter_by(estado_compra=EstadoCompra.SATISFECHA).all()

        if not ordenes:
            return {"mensaje" : "no hay ordenes satisfechas"}
        
        return self.orden_schema.dump(ordenes, many=True)
    
    def actualizar_orden_de_compra(self, nro_orden, descripcion, cod_orden, estado_compra):
        """
        Actualiza una orden de compra.
        
        :param nro_orden: Número de la orden de compra.
        :param descripcion: Nueva descripción de la orden de compra.
        :param cod_orden: Nuevo código de la orden de compra.
        :return: La orden de compra actualizada.
        """
        try:
            orden = OrdenDeCompra.query.get(nro_orden)
            if not orden:
                return {"error": "Orden de compra no encontrada"}

            orden.descripcion = descripcion
            orden.cod_orden = cod_orden
            orden.estado_compra = EstadoCompra[estado_compra]

            db.session.commit()
            return self.orden_schema.dump(orden)
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}
        
        except KeyError:
            return {"error": "Estado de compra no válido"}
        
    def actualizar_detalle_orden_de_compra(self, id_detalle, cantidad_requerida, precio_material):
        """
        Actualiza un detalle de la orden de compra.
        
        :param nro_orden: Número de la orden de compra.
        :param id_material: ID del material a actualizar.
        :param cantidad_requerida: Nueva cantidad requerida.
        :param precio_material: Nuevo precio del material.
        :return: Detalle actualizado.
        """
        try:
            detalle = DetalleOrdenCompra.query.get(id_detalle)
            if not detalle:
                return {"error": "Detalle de orden no encontrado"}

            detalle.cantidad_requerida = cantidad_requerida
            detalle.precio_material = precio_material

            db.session.commit()
            return self.detalle_schema.dump(detalle)
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}    
        
    def eliminar_orden_de_compra(self, nro_orden):
        """
        Elimina una orden de compra y sus detalles.
        
        :param nro_orden: Número de la orden de compra.
        :return: Mensaje de éxito o error.
        """
        try:
            orden = OrdenDeCompra.query.get(nro_orden)
            if not orden:
                return {"error": "Orden de compra no encontrada"}

            # Eliminar los detalles de la orden
            DetalleOrdenCompra.query.filter_by(nro_orden=nro_orden).delete()

            # Eliminar la orden de compra
            db.session.delete(orden)
            db.session.commit()
            return {"message": "Orden de compra eliminada exitosamente"}
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}
        
    def eliminar_detalle_orden(self, detalle_id):
        """
        Elimina un detalle de orden de compra.
        
        :param detalle_id: ID del detalle de orden de compra.
        :return: Mensaje de éxito o error.
        """
        try:
            detalle = DetalleOrdenCompra.query.get(detalle_id)
            if not detalle:
                return {"error": "Detalle de orden de compra no encontrado"}
            
            db.session.delete(detalle)
            db.session.commit()
            return {"message": "Detalle de orden de compra eliminado exitosamente"}
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}