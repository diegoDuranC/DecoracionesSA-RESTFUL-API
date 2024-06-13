from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app import db
from models.material.material import Material

from models.compras.nota_de_entrega import NotaDeEntrega, NotaDeEntregaSchema
from models.compras.material_recibido import MaterialRecibido, MaterialRecibidoSchema

from models.compras.orden_de_compra import OrdenDeCompra, EstadoCompra
from models.material.transacciones_inventario import TransaccionInventario

class NotaDeEntregaFacade:

    def __init__(self):
        self.nota_de_entrega_schema = NotaDeEntregaSchema()
        self.nota_de_entrega_schemas = NotaDeEntregaSchema(many=True)
        self.material_recibido_schema = MaterialRecibidoSchema()
        self.material_recibido_schemas = MaterialRecibidoSchema(many=True)

    def obtener_todas_las_notas_de_entrega(self):
        notas = NotaDeEntrega.query.all()

        if not notas:
            return {"Error": "No hay notas"}
        
        return self.nota_de_entrega_schemas.dump(notas)

    def obtener_nota_de_entrega(self, nro_nota):
        nota = NotaDeEntrega.query.get(nro_nota)

        if not nota:
            return {"Error": "No se encontró la nota"}
        return self.nota_de_entrega_schema.dump(nota)    

    def agregar_nota_de_entrega(self, nro_orden, materiales_recibidos):
        try:
            orden = OrdenDeCompra.query.get(nro_orden)
            if not orden:
                return {"Error": "Orden de compra no encontrada"}

            if orden.estado_compra == EstadoCompra.SATISFECHA:
                return {"Mensaje": "La orden ya fue satisfecha"}

            for material in materiales_recibidos:
                id_material = material.get('id_material')
                cantidad_recibida = material.get('cantidad_recibida')

                detalle = next((detalle for detalle in orden.detalles if detalle.id_material == id_material), None)
                if not detalle:
                    return {"Error": f"Material ID {id_material} no encontrado en la orden"}

                cantidad_requerida = detalle.cantidad_requerida
                cantidad_recibida_actual = sum(
                    m.cantidad_recibida for nota in orden.notas_entrega 
                    for m in nota.materiales_recibidos 
                    if m.id_material == id_material
                )

                if cantidad_recibida > cantidad_requerida:
                    return {"Error": f"La cantidad recibida de material ID {id_material} excede la cantidad requerida"}

                cantidad_faltante = cantidad_requerida - cantidad_recibida_actual
                if cantidad_recibida > cantidad_faltante:
                    return {"Error": f"La cantidad recibida de material ID {id_material} excede la cantidad faltante por recibir"}

            nueva_nota = NotaDeEntrega(nro_orden=nro_orden)
            db.session.add(nueva_nota)
            db.session.flush()

            for material in materiales_recibidos:
                id_material = material.get('id_material')
                cantidad_recibida = material.get('cantidad_recibida')

                nuevo_material_recibido = MaterialRecibido(
                    id_material=id_material,
                    cantidad_recibida=cantidad_recibida,
                    nro_nota=nueva_nota.nro_nota
                )

                db.session.add(nuevo_material_recibido)

                # Verificar si los materiales recibidos se están guardando correctamente
                print(f"Material recibido guardado: {nuevo_material_recibido}")

                material_actualizado = Material.query.get(id_material)
                if material_actualizado:
                    material_actualizado.existencias += cantidad_recibida

                    codigo_transaccion = f"{nuevo_material_recibido.id}-E"
                    nueva_transaccion = TransaccionInventario(
                        codigo_transaccion=codigo_transaccion,
                        fecha_transaccion=nueva_nota.fecha,
                        id_material=id_material,
                        descripcion=material_actualizado.descripcion,
                        precio_unitario=material_actualizado.precio_unitario,
                        cantidad_entrada=cantidad_recibida,
                        cantidad_salida=0,
                        existencia_salida=material_actualizado.existencias,
                        material_recibido_id=nuevo_material_recibido.id
                    )
                    db.session.add(nueva_transaccion)

            db.session.flush()
            self._actualizar_estado_orden(orden, nueva_nota)

            db.session.commit()
            return self.nota_de_entrega_schema.dump(nueva_nota)

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"Error": str(e)}
        
    def _actualizar_estado_orden(self, orden, nota_actual):
        todos_materiales_completos = True

        for detalle in orden.detalles:
            cantidad_requerida = detalle.cantidad_requerida
            cantidad_recibida = sum(material.cantidad_recibida for material in nota_actual.materiales_recibidos if material.id_material == detalle.id_material)

            # Verificar la cantidad recibida para cada material
            print(f"Material ID {detalle.id_material}: cantidad requerida = {cantidad_requerida}, cantidad recibida = {cantidad_recibida}")

            if cantidad_recibida < cantidad_requerida:
                todos_materiales_completos = False
                print(f"Falta recibir materiales para el detalle del material ID {detalle.id_material}.")
                break

            # Actualizar el estado de la orden inmediatamente
            if todos_materiales_completos:
                orden.estado_compra = EstadoCompra.SATISFECHA
                print(f"Todos los materiales están completos. Orden {orden.nro_orden} satisfecha.")
            else:
                orden.estado_compra = EstadoCompra.PARCIALMENTE_SATISFECHA
                print(f"Faltan materiales por recibir. Orden {orden.nro_orden} parcialmente satisfecha.")

        # Actualizar el estado de la orden en la base de datos
        db.session.add(orden)
        db.session.flush()

    def eliminar_nota_de_entrega(self, nro_nota):
        try:
            nota = NotaDeEntrega.query.get(nro_nota)
            if not nota:
                return {"Error": "Nota de entrega no encontrada"}

            orden = nota.orden_de_compra

            for material_recibido in nota.materiales_recibidos:
                material = Material.query.get(material_recibido.id_material)
                if material:
                    material.existencias -= material_recibido.cantidad_recibida

                transaccion = TransaccionInventario.query.filter_by(material_recibido_id=material_recibido.id).first()
                if transaccion:
                    db.session.delete(transaccion)

                db.session.delete(material_recibido)

            db.session.delete(nota)
            db.session.flush()
            self._actualizar_estado_orden(orden)

            db.session.commit()
            return {"Mensaje": "Nota de entrega eliminada correctamente"}
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"Error": str(e)}