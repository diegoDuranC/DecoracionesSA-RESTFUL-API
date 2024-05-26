from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app import db
from models.material.material import Material
from models.compras.nota_de_entrega import NotaDeEntrega, NotaDeEntregaSchema
from models.compras.entrega_pendiente import EntregaPendiente, EntregaPendienteSchema, EstadoEntrega
from models.compras.detalle_material_pendiente import DetalleMaterialPendiente, DetalleMaterialPendienteSchema
from models.compras.material_recibido import MaterialRecibido, MaterialRecibidoSchema
from models.compras.orden_de_compra import OrdenDeCompra
from models.material.transacciones_inventario import TransaccionInventario

class NotaDeEntregaFacade:
    def __init__(self):
        self.nota_de_entrega_schema = NotaDeEntregaSchema()
        self.nota_de_entrega_schemas = NotaDeEntregaSchema(many=True)
        self.entrega_pendiente_schema = EntregaPendienteSchema()
        self.entrega_pendiente_schemas = EntregaPendienteSchema(many=True)
        self.detalle_material_pendiente_schema = DetalleMaterialPendienteSchema()
        self.detalle_material_pendiente_schemas = DetalleMaterialPendienteSchema(many=True)
        self.material_recibido_schema = MaterialRecibidoSchema()
        self.material_recibido_schemas = MaterialRecibidoSchema(many=True)

    # def crear_nota_de_entrega(self, data):
    #     nueva_nota = NotaDeEntrega(nro_orden=data['nro_orden'])
    #     db.session.add(nueva_nota)
    #     db.session.commit()
    #     return self.nota_de_entrega_schema.dump(nueva_nota)

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

    # def crear_entrega_pendiente(self, data):
    #     nueva_entrega = EntregaPendiente(nro_nota=data['nro_nota'])
    #     db.session.add(nueva_entrega)
    #     db.session.commit()
        
    #     for detalle in data['detalles']:
    #         nuevo_detalle = DetalleMaterialPendiente(
    #             cod_material=detalle['cod_material'],
    #             cantidad_pendiente=detalle['cantidad_pendiente'],
    #             descripcion=detalle['descripcion'],
    #             entrega_pendiente_id=nueva_entrega.id_entrega_pendiente
    #         )
    #         db.session.add(nuevo_detalle)
        
    #     db.session.commit()
    #     return self.entrega_pendiente_schema.dump(nueva_entrega)

    # def obtener_todas_las_entregas_pendientes(self):
    #     entregas = EntregaPendiente.query.all()
    #     return self.entrega_pendiente_schemas.dump(entregas)
    
    def obtener_entrega_pendiente_nro_nota(self, nro_nota):
        entrega = EntregaPendiente.query.filter_by(nro_nota=nro_nota).first()
        if not entrega:
            return {"Error": "No se encontró la entrega pendiente"}
        return self.entrega_pendiente_schema.dump(entrega)

    # def actualizar_entrega_pendiente(self, id, data):
    #     entrega = EntregaPendiente.query.get(id)
    #     if not entrega:
    #         return {'message': 'EntregaPendiente not found'}, 404

    #     entrega.estado = data.get('estado', entrega.estado)
    #     entrega.fecha_actualizacion = datetime.now().strftime("%Y-%m-%d")

    #     db.session.commit()
    #     return self.entrega_pendiente_schema.dump(entrega)
        
    def agregar_nota_de_entrega(self, nro_orden, materiales_recibidos):
        try:
            orden = OrdenDeCompra.query.get(nro_orden)
            if not orden:
                return {"Error": "Orden de compra no encontrada"}

            nueva_nota = NotaDeEntrega(nro_orden=nro_orden)
            db.session.add(nueva_nota)
            db.session.flush()

            total_diferencia = 0
            nueva_entrega_pendiente = None

            for material in materiales_recibidos:
                cod_material = material.get('cod_material')
                cantidad_recibida = material.get('cantidad_recibida')

                nuevo_material_recibido = MaterialRecibido(
                    cod_material=cod_material,
                    cantidad_recibida=cantidad_recibida,
                    nro_nota=nueva_nota.nro_nota
                )
                db.session.add(nuevo_material_recibido)

                material_actualizado = Material.query.get(cod_material)
                if material_actualizado:
                    material_actualizado.existencias += cantidad_recibida

                    # Crear transacción de inventario
                    codigo_transaccion = f"{nuevo_material_recibido.id}-E"
                    nueva_transaccion = TransaccionInventario(
                        codigo_transaccion=codigo_transaccion,
                        codigo_material=cod_material,
                        descripcion=material_actualizado.descripcion,
                        precio_unitario=material_actualizado.precio_unitario,
                        fecha_transaccion=nueva_nota.fecha,
                        cantidad_entrada=cantidad_recibida,
                        cantidad_salida=0,
                        existencia_salida=material_actualizado.existencias
                    )
                    db.session.add(nueva_transaccion)

                detalle_orden = next((d for d in orden.detalles if d.codigo_material == cod_material), None)
                if detalle_orden:
                    diferencia = detalle_orden.cantidad_requerida - cantidad_recibida
                    total_diferencia += diferencia

                    if diferencia > 0:
                        if not nueva_entrega_pendiente:
                            nueva_entrega_pendiente = EntregaPendiente(
                                fecha_actualizacion=datetime.now().strftime("%Y-%m-%d"),
                                nro_nota=nueva_nota.nro_nota,
                                estado=EstadoEntrega.PENDIENTE
                            )
                            db.session.add(nueva_entrega_pendiente)
                            db.session.flush()

                        nuevo_detalle_material_pendiente = DetalleMaterialPendiente(
                            cod_material=cod_material,
                            cantidad_pendiente=diferencia,
                            descripcion=material_actualizado.descripcion,
                            entrega_pendiente_id=nueva_entrega_pendiente.id_entrega_pendiente
                        )
                        db.session.add(nuevo_detalle_material_pendiente)

            if nueva_entrega_pendiente and total_diferencia == 0:
                nueva_entrega_pendiente.estado = EstadoEntrega.ENTREGADO

            db.session.commit()
            nueva_transaccion.codigo_transaccion = f"{nueva_nota.nro_nota}-E"

            return self.nota_de_entrega_schema.dump(nueva_nota)
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"Error": str(e)}
        
        #         if diferencia > 0:
            #             if not nueva_entrega_pendiente:
            #                 nueva_entrega_pendiente = EntregaPendiente(
            #                     fecha_actualizacion=datetime.now().strftime("%Y-%m-%d"),
            #                     nro_nota=nueva_nota.nro_nota,
            #                     estado=EstadoEntrega.PENDIENTE
            #                 )
            #                 db.session.add(nueva_entrega_pendiente)
            #                 db.session.flush()

            #             nuevo_detalle_material_pendiente = DetalleMaterialPendiente(
            #                 cod_material=cod_material,
            #                 cantidad_pendiente=diferencia,
            #                 descripcion=material_actualizado.descripcion,
            #                 entrega_pendiente_id=nueva_entrega_pendiente.id_entrega_pendiente
            #             )
            #             db.session.add(nuevo_detalle_material_pendiente)

            # if nueva_entrega_pendiente and total_diferencia == 0:
            #     nueva_entrega_pendiente.estado = EstadoEntrega.ENTREGADO