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

    def _actualizar_estado_orden(self, orden):
        todos_materiales_completos = True
        cantidades_totales_recibidas = {}

        if not orden.notas_entrega:
            orden.estado_compra = EstadoCompra.PENDIENTE
            db.session.commit()

        print(f"Procesando orden {orden.nro_orden} con notas de entrega: {orden.notas_entrega}")

        # Recorrer todas las notas de entrega de la orden
        for nota in orden.notas_entrega:
            print(f"Procesando nota de entrega {nota.nro_nota}")
            for material_recibido in nota.materiales_recibidos:
                print(f"Procesando material recibido ID {material_recibido.id_material} con cantidad {material_recibido.cantidad_recibida}")
                material_id = material_recibido.id_material
                cantidad_recibida_total = material_recibido.cantidad_recibida

                # Acumular la cantidad recibida por material
                if material_id not in cantidades_totales_recibidas:
                    cantidades_totales_recibidas[material_id] = 0
                cantidades_totales_recibidas[material_id] += cantidad_recibida_total

        # Imprimir las cantidades totales recibidas para depuración
        print(f"cantidades_totales_recibidas: {cantidades_totales_recibidas}")

        # Revisar cada detalle de la orden para ver si se ha recibido la cantidad requerida
        for detalle in orden.detalles:
            cantidad_requerida = detalle.cantidad_requerida
            cantidad_recibida = cantidades_totales_recibidas.get(detalle.id_material, 0)

            print(f"Material ID {detalle.id_material}: cantidad requerida = {cantidad_requerida}, cantidad recibida = {cantidad_recibida}")

            if cantidad_recibida < cantidad_requerida:
                todos_materiales_completos = False
                print(f"Falta recibir materiales para el detalle del material ID {detalle.id_material}.")
                break

        # Actualizar el estado de la orden basado en las cantidades recibidas
        if todos_materiales_completos:
            orden.estado_compra = EstadoCompra.SATISFECHA
            print(f"Todos los materiales están completos. Orden {orden.nro_orden} satisfecha.")
        elif any(cantidades_totales_recibidas.values()):
            orden.estado_compra = EstadoCompra.PARCIALMENTE_SATISFECHA
            print(f"Faltan materiales por recibir. Orden {orden.nro_orden} parcialmente satisfecha.")
        else:
            orden.estado_compra = EstadoCompra.PENDIENTE
            print(f"No se ha recibido ningún material. Orden {orden.nro_orden} pendiente.")

        db.session.add(orden)
        db.session.flush()
        

    def agregar_nota_de_entrega(self, nro_orden, materiales_recibidos):
        try:
            orden = OrdenDeCompra.query.get(nro_orden)
            if not orden:
                return {"Error": "Orden de compra no encontrada"}

            if orden.estado_compra == EstadoCompra.SATISFECHA:
                return {"Mensaje": "La orden ya fue satisfecha"}

            nueva_nota = NotaDeEntrega(nro_orden=nro_orden)
            db.session.add(nueva_nota)
            db.session.flush()

            for material in materiales_recibidos:
                id_material = material.get('id_material')
                cantidad_recibida = material.get('cantidad_recibida')

                material_recibido = MaterialRecibido(
                    nro_nota=nueva_nota.nro_nota,
                    id_material=id_material,
                    cantidad_recibida=cantidad_recibida
                )
                db.session.add(material_recibido)

                material_db = Material.query.get(id_material)
                material_db.existencias += cantidad_recibida

            db.session.flush()

            # Llamar a la función para actualizar el estado de la orden
            self._actualizar_estado_orden(orden)

            db.session.commit()
            return {"Mensaje": "Nota de entrega agregada correctamente"}

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"Error": str(e)}



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

            # Actualizar el estado de la orden después de eliminar la nota
            self._actualizar_estado_orden(orden)

            db.session.commit()
            return {"Mensaje": "Nota de entrega eliminada correctamente"}

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"Error": str(e)}


