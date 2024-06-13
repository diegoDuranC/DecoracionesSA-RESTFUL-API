from models.material.transacciones_inventario import TransaccionInventario, TransaccionInventarioSchema
# from app import db

class TransaccionInventarioFacade:
    def __init__(self):
        self.transaccion_inventario_schema = TransaccionInventarioSchema()
        self.transaccion_inventario_schemas = TransaccionInventarioSchema(many=True)

    def obtener_todas_las_transacciones(self):
        transacciones = TransaccionInventario.query.all()
        return self.transaccion_inventario_schemas.dump(transacciones)

    def obtener_transacciones_por_fecha(self, fecha_inicio, fecha_fin):
        transacciones = TransaccionInventario.query.filter(
            TransaccionInventario.fecha_transaccion.between(fecha_inicio, fecha_fin)
        ).all()
        return self.transaccion_inventario_schemas.dump(transacciones)

    def obtener_transacciones_por_codigo_material(self, codigo_material):
        transacciones = TransaccionInventario.query.filter_by(codigo_material=codigo_material).all()
        return self.transaccion_inventario_schemas.dump(transacciones)

    def obtener_transaccion_por_id(self, id):
        transaccion = TransaccionInventario.query.get(id)
        if not transaccion:
            return {"Error": "Transacción no encontrada"}
        return self.transaccion_inventario_schema.dump(transaccion)

    def obtener_transacciones_entrada_por_codigo_material(self, codigo_material):
        transacciones = TransaccionInventario.query.filter(
            TransaccionInventario.codigo_material == codigo_material,
            TransaccionInventario.tipo_transaccion == 'E'  # Assuming 'E' denotes Entrada
        ).all()
        return self.transaccion_inventario_schemas.dump(transacciones)

    def obtener_transacciones_salida_por_codigo_material(self, codigo_material):
        transacciones = TransaccionInventario.query.filter(
            TransaccionInventario.codigo_material == codigo_material,
            TransaccionInventario.tipo_transaccion == 'S'  # Assuming 'S' denotes Salida
        ).all()
        return self.transaccion_inventario_schemas.dump(transacciones)
    
    # def actualizar_transaccion(self, id, data):
    #     try:
    #         transaccion = TransaccionInventario.query.get(id)
    #         if not transaccion:
    #             return {"Error": "Transacción no encontrada"}, 404

    #         if 'codigo_material' in data:
    #             transaccion.codigo_material = data['codigo_material']
    #         if 'descripcion' in data:
    #             transaccion.descripcion = data['descripcion']
    #         if 'precio_unitario' in data:
    #             transaccion.precio_unitario = data['precio_unitario']
    #         if 'fecha_transaccion' in data:
    #             transaccion.fecha_transaccion = data['fecha_transaccion']
    #         if 'cantidad_entrada' in data:
    #             transaccion.cantidad_entrada = data['cantidad_entrada']
    #         if 'cantidad_salida' in data:
    #             transaccion.cantidad_salida = data['cantidad_salida']
    #         if 'existencia_salida' in data:
    #             transaccion.existencia_salida = data['existencia_salida']
    #         if 'tipo_transaccion' in data:
    #             transaccion.tipo_transaccion = data['tipo_transaccion']

    #         db.session.commit()
    #         return self.transaccion_inventario_schema.dump(transaccion)
        
    #     except SQLAlchemyError as e:
    #         db.session.rollback()
    #         return {"Error": str(e)}, 500