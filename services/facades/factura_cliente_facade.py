from models.cliente.factura_cliente import FacturaCliente
from models.cliente.detalle_factura import DetalleFactura
from models.requisicion.requisicion import Requisicion
from models.requisicion.detalle_materiales import DetalleMaterialRequisicion
from models.material.material import Material
from models.cliente.cliente import Cliente
from models.proyecto import Proyecto
from app import db
from decimal import Decimal


from models.cliente.factura_cliente import FacturaCliente, FacturaSchema

factura_schema = FacturaSchema()
factura_schemas = FacturaSchema(many=True)

#costo_mano_de_obra suma de costo en todas las requisiciones
#direccion_envio direccion del cliente

class FacturaClienteFacade():

    def crear_factura(self, nro_proyecto):
        proyecto = Proyecto.query.get(nro_proyecto)
        
        if proyecto is None:
            return {"Error" : "No existe el proyecto"}
        
        cliente = Cliente.query.get(proyecto.cliente_id)
        
        cliente_id = cliente.ID_cliente
        direccion_envio = cliente.direccion_cliente
        proyecto_id = proyecto.nro_proyecto
        total_materiales = Decimal('0.00')
        costo_mano_de_obra = Decimal('0.00')
        
        #CALCULAR MANO DE OBRA TOTAL
        requisiciones = Requisicion.query.filter_by(proyecto_nro_proyecto=nro_proyecto)

        for requisicion in requisiciones:
            #CALCULA EL COSTO DE MANO DE OBRA TOTAL POR REQUISICION
            if requisicion.costo is not None:
                costo_mano_de_obra += Decimal(str(requisicion.costo))
            
        factura = FacturaCliente(
            costo_mano_obra= float(costo_mano_de_obra),
            direccion_envio=direccion_envio,
            cliente_id=cliente_id,
            proyecto_id=proyecto_id,
            total = costo_mano_de_obra
        )

        db.session.add(factura)
        db.session.commit()

        for requisicion in requisiciones:
            detalle_materiales = DetalleMaterialRequisicion.query.filter_by(nro_requisicion=requisicion.nro_requisicion).all()
            detalles_list = []

            for detalle in detalle_materiales:
                material = Material.query.get(detalle.id_material)

                cod_material = material.cod_material
                nombre_material = material.descripcion
                precio_unitario = Decimal(str(material.precio_unitario))
                cantidad = Decimal(str(detalle.cantidad_solicitada))
                sub_total = cantidad*precio_unitario

                total_materiales += sub_total

                detalle_factura = DetalleFactura(
                    nro_factura = factura.nro_factura,
                    cod_material = cod_material,
                    nombre_material = nombre_material,
                    precio_unitario = float(precio_unitario),
                    cantidad = float(cantidad),
                    sub_total = sub_total
                )
                detalles_list.append(detalle_factura)
            db.session.add_all(detalles_list)

        factura.total += total_materiales
        db.session.add(factura)
        db.session.commit()
        
        return factura_schema.dump(factura)
    
    def get_facturas(self):
        consulta = FacturaCliente.query.all()
        return factura_schemas.dump(consulta)

    def get_facturas_cliente_id(self, cliente_id):
        facturas = FacturaCliente.query.filter_by(cliente_id=cliente_id).all()

        if not facturas:
            return {"error": "El cliente no tiene facturas"}
        
        return factura_schemas.dump(facturas)

    def get_facturas_cliente_ci(self, ci_cliente):   
        cliente = Cliente.query.filter_by(ci_cliente=ci_cliente).first()

        if not cliente:
            return {"error" : "el cliente no existe"}
        
        facturas = FacturaCliente.query.filter_by(cliente_id=cliente.ID_cliente).all()

        if not facturas: return {"mensaje" : "El cliente no tiene facturas"}

        return factura_schemas.dump(facturas)
    
    def actualizar_factura(self, nro_factura, monto, fecha, descripcion, nro_deposito):
        factura = FacturaCliente.query.get(nro_factura)

        if factura:
            factura.monto = monto
            factura.fecha = fecha
            factura.descripcion = descripcion
            factura.nro_deposito = nro_deposito

            db.session.commit()

            return factura_schema.dump(factura)
        
        return {'message': 'Factura no encontrada'}, 404

    def eliminar_factura(self, nro_factura):
        factura = FacturaCliente.query.get(nro_factura)
        if factura:
            db.session.delete(factura)
            db.session.commit()
            return {'message': 'Factura eliminada exitosamente'}
        
        return {'message': 'Factura no encontrada'}, 404