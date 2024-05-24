from models.cliente.factura_cliente import FacturaCliente
from models.cliente.detalle_factura import DetalleFactura
from models.requisicion.requisicion import Requisicion
from models.requisicion.detalle_materiales import DetalleMaterialRequisicion
from models.material.material import Material
from models.cliente.cliente import Cliente
from models.proyecto import Proyecto
from app import db
from decimal import Decimal

#costo_mano_de_obra suma de costo en todas las requisiciones
#direccion_envio direccion del cliente

class FacturaClienteFacade():

    def crear_factura(self, nro_proyecto):
        proyecto = Proyecto.query.get(nro_proyecto)

        if proyecto is None:
            return {"Error" : "No existe el proyecto"}
        cliente = Cliente.query.get(proyecto.cliente_id)
        
        cliente_id = cliente.id_cliente
        direccion_envio = cliente.direccion_cliente
        proyecto_id = proyecto.numero_proyecto
        total_materiales = Decimal('0.00')
        costo_mano_de_obra = Decimal('0.00')
        
        #CALCULAR MANO DE OBRA TOTAL
        #requisiciones = requisicion_facade.get_requisiciones(nro_proyecto)
        requisiciones = Requisicion.query.filter_by(proyecto_id=nro_proyecto)

        for requisicion in requisiciones:

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
                material = Material.query.get(detalle.codigo_material)

                cod_material = detalle.codigo_material
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
                # db.session.add(detalle_factura)
                detalles_list.append(detalle_factura)
            db.session.add_all(detalles_list)

        factura.total += total_materiales
        db.session.add(factura)
        db.session.commit()
        
        return factura
    
    def get_facturas(self):
        return FacturaCliente.query.all()

    def get_facturas_cliente(self, cliente_id):
        return FacturaCliente.query.filter_by(cliente_id=cliente_id)
    