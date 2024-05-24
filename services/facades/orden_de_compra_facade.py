from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app import db
from models.material.material import Material
from models.compras.orden_de_compra import OrdenDeCompra, OrdenDeCompraSchema
from models.compras.detalle_orden import DetalleOrdenCompra, DetalleOrdenCompraSchema
from models.compras.nota_entrega import NotaDeEntrega

class OrdenDeCompraFacade:

    def __init__(self):
        self.orden_schema = OrdenDeCompraSchema()
        self.detalle_schema = DetalleOrdenCompraSchema()

    def crear_orden_de_compra(self, descripcion, materiales):
        """
        Crea una orden de compra con los materiales requeridos.
        
        :param descripcion: Descripción de la orden de compra.
        :param materiales: Lista de materiales y sus cantidades requeridas. 
                           Formato: [{'codigo_material': 1, 'cantidad_requerida': 10, 'precio_material': 50.00}, ...]
        :return: La orden de compra creada.
        """
        try:
            # Crear la orden de compra
            nueva_orden = OrdenDeCompra(descripcion=descripcion)
            db.session.add(nueva_orden)
            db.session.flush()  # Asegura que se genere el nro_orden
            
            # Crear los detalles de la orden de compra
            for material_data in materiales:
                codigo_material = material_data.get('codigo_material')
                cantidad_requerida = material_data.get('cantidad_requerida')
                precio_material = material_data.get('precio_material')
                
                material = Material.query.get(codigo_material)
                if not material:
                    return {"Error": f"Material con código {codigo_material} no encontrado"}

                detalle = DetalleOrdenCompra(
                    cantidad_requerida=cantidad_requerida,
                    precio_material=precio_material,
                    codigo_material=codigo_material,
                    nro_orden=nueva_orden.nro_orden
                )
                db.session.add(detalle)
                
                # Actualizar el inventario
                material.existencias += cantidad_requerida
            
            db.session.commit()
            return self.orden_schema.dump(nueva_orden)
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"Error": str(e)}
        
    def obtener_orden_por_id(self, nro_orden):
        """
        Obtiene una orden de compra por su número de orden.
        
        :param nro_orden: Número de la orden de compra.
        :return: La orden de compra y sus detalles.
        """
        orden = OrdenDeCompra.query.get(nro_orden)
        if not orden:
            return {"Error": "Orden de compra no encontrada"}
        
        detalles = DetalleOrdenCompra.query.filter_by(nro_orden=nro_orden).all()
        return {
            "orden": self.orden_schema.dump(orden),
            "detalles": self.detalle_schema.dump(detalles, many=True)
        }

    def obtener_todas_las_ordenes(self):
        """
        Obtiene todas las órdenes de compra.
        
        :return: Lista de todas las órdenes de compra.
        """
        ordenes = OrdenDeCompra.query.all()
        return self.orden_schema.dump(ordenes, many=True)
    
    def agregar_nota_de_entrega(self, nro_orden, fecha):
        try:
            orden = OrdenDeCompra.query.get(nro_orden)
            if not orden:
                return {"Error": "Orden de compra no encontrada"}

            nueva_nota = NotaDeEntrega(nro_orden=nro_orden, fecha=fecha)
            db.session.add(nueva_nota)
            
            # Aquí podrías agregar lógica adicional para verificar físicamente los materiales
            # Por ejemplo, podrías recorrer los detalles de la orden y realizar alguna verificación

            db.session.commit()
            return self.nota_schema.dump(nueva_nota)
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"Error": str(e)}