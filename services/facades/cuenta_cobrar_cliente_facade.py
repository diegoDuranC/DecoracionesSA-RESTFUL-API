from decimal import Decimal
from models.cliente.factura_cliente import FacturaCliente
from models.cliente.cuenta_cobrar import CuentaPorCobrar, CuentaPorCobrarSchema, EstadoCuentaSchema
from models.cliente.plan_pago_cliente import PlanPagoCliente, PlanPagoClienteSchema
from models.cliente.cliente import Cliente

from datetime import datetime, timedelta
from utils.date_utils import format_date

from app import db

'''
    datos necesarios para generar un plan de credito
    amortizacion = cantidad de cuotas 
    vencimiento = fecha (dada por el empleado)
'''

class CuentaPorCobrarClienteFacade():

    ''' campos Cuenta
        importe
        saldo
        fecha_creacion
        vencimiento
        amortizacion
    '''
 
    def generar_plan_pago(self, cuenta_id, fecha_creacion, importe, intervalo_pago, vencimiento):
        '''
            Datos por instancia de plan de pagos:
                fecha
                monto
                nro_cuenta

            Parámetros necesarios:

            importe (Total de la factura)
            fecha_creacion (Sacado de la fecha_creacion de la cuenta)
            vencimiento (Sacado del request)
            intervalo_pago (Dato del request con intervalo con valores enteros que representan los dias ejemplo: quincenal = 15, mensual = 30, etc)

            Retorna el vencimiento de ultimo pago, es decir, el vencimiento, y el campo amortizacion la cantidad de instancias de PlanPagoCliente
        '''
        
        importe = Decimal(importe)
        intervalo_pago_dias = int(intervalo_pago)
        fecha_creacion_dt = fecha_creacion
        vencimiento_dt = datetime.strptime(vencimiento, "%Y-%m-%d").date()

        # Calcular la cantidad de días hasta el vencimiento
        dias_hasta_vencimiento = (vencimiento_dt - fecha_creacion_dt).days

        # Calcular la cantidad de pagos
        amortizacion = dias_hasta_vencimiento // intervalo_pago_dias

        if dias_hasta_vencimiento % intervalo_pago_dias != 0:
            amortizacion += 1

        # Calcular el monto de cada pago, distribuyendo equitativamente
        monto_pago = importe / amortizacion

        # Lista de pagos
        plan_pagos = []

        # Fecha del primer pago a la fecha de creacion se le aumenta la cantidad de dias para el siguiente o el intervalo
        fecha_pago = fecha_creacion_dt + timedelta(days=intervalo_pago_dias)

        # Generar los planes de pagos
        for i in range(amortizacion):
            # Si es el último pago, ajustar la fecha de pago al vencimiento exacto
            if i == amortizacion - 1:
                fecha_pago = vencimiento_dt
            
            plan_pago = PlanPagoCliente(
                nro_cuenta=cuenta_id,
                fecha=fecha_pago,
                monto=monto_pago
            )
            
            plan_pagos.append(plan_pago)

            # Calcular la fecha del próximo pago sumando el intervalo de pago
            fecha_pago += timedelta(days=intervalo_pago_dias)

        ultimo_pago_fecha = plan_pagos[-1].fecha

        db.session.add_all(plan_pagos)
        db.session.commit()

        return amortizacion, ultimo_pago_fecha

    def generar_cuenta_por_cobrar(self, request_data, nro_factura):

        cuenta_schema = CuentaPorCobrarSchema()
        factura = FacturaCliente.query.get(nro_factura)

        if not factura:
            return {"Error" : "Factura no encontrada"}

        cuenta = CuentaPorCobrar(
            importe = factura.total,
            saldo = factura.total,
            fecha_creacion = factura.fecha,
            id_cliente = factura.cliente_id,
            nro_factura = nro_factura
        )

        db.session.add(cuenta)
        db.session.commit()

        if request_data:
            #VENCIMIENTO ES LA FECHA TOPE PARA VENCER LA DEUDA
            #SE ACEPTAN PAGOS QUINCENALES ES DECIR 2 VECES AL MES, O MENSUALES
            vencimiento = format_date(request_data.get('vencimiento'))
            nro_cuenta = cuenta.nro_cuenta

            'Crear el plan de pagos'      
            amortizacion_plan , ultimo_pago_fecha = self.generar_plan_pago(
                cuenta_id=nro_cuenta,
                fecha_creacion=cuenta.fecha_creacion,
                vencimiento=vencimiento,
                importe=cuenta.importe,
                intervalo_pago=request_data.get('intervalo_pago_dias')
            )

            cuenta.amortizacion = amortizacion_plan
            cuenta.vencimiento = ultimo_pago_fecha

            db.session.commit()
        
            return cuenta_schema.dump(cuenta)

        else:
            cuenta.vencimiento = factura.fecha

            db.session.commit()
            
            return cuenta_schema.dump(cuenta)

    def get_cuentas_cliente(self, id_cliente):
        '''
            dado un id de cliente se devuelve todas las cuentas de este, cada una con su lista de pagos
        '''
        cuenta_schema = CuentaPorCobrarSchema(many=True)
        cuentas = CuentaPorCobrar.query.filter_by(id_cliente=id_cliente).all()

        if not cuentas:
            return {"Mensaje" : "El cliente no tiene cuentas"}
        
        else:
            return cuenta_schema.dump(cuentas)
        
    def get_cuentas_cobrar(self):

        cuentas_schema = CuentaPorCobrarSchema(many=True)
        cuentas = CuentaPorCobrar.query.all()

        if not cuentas:
            return {"Error" : "No hay cuentas"}
        
        return cuentas_schema.dump(cuentas)
    
    def get_cuentas_cobrar_ci_pendientes(self, ci_cliente):
         
        """
        Obtiene todas las cuentas por cobrar de un cliente que tengan saldo mayor a 0.
        
        :param ci_cliente: CI del cliente.
        :return: Lista de cuentas por cobrar con saldo mayor a 0.
        """
        cuentas_schema = CuentaPorCobrarSchema(many=True)

        cliente = Cliente.query.filter_by(ci_cliente=ci_cliente).first()

        if not cliente:
            return {"Error": "Cliente no encontrado"}

        cuentas_con_saldo = CuentaPorCobrar.query.filter(
            CuentaPorCobrar.id_cliente == cliente.id_cliente,
            CuentaPorCobrar.saldo > 0
        ).all()

        if not cuentas_con_saldo:
            #print(cliente.ci_cliente)
            return {"Error": "No hay cuentas por cobrar con saldo para este cliente"}

        return cuentas_schema.dump(cuentas_con_saldo)

    def generar_estado_cuenta(self, nro_cuenta):
        cuenta = CuentaPorCobrar.query.get(nro_cuenta)

        cuenta_schema = EstadoCuentaSchema()
        if not cuenta: 
            return {"Error" : "No hay cuenta"}
        
        return cuenta_schema.dump(cuenta)
    
    def eliminar_cuenta_pagos(self, nro_cuenta):
        try:
            # Se busca la cuenta por cobrar en la base de datos
            cuenta_por_cobrar = CuentaPorCobrar.query.filter_by(nro_cuenta=nro_cuenta).first()

            # Si la cuenta no se encuentra, se retorna False
            if not cuenta_por_cobrar:
                return {"error" : "La cuenta no existe"}

            # Se eliminan todos los pagos asociados a la cuenta
            for pago in cuenta_por_cobrar.pagos:
                db.session.delete(pago)

            # Se elimina la cuenta por cobrar
            db.session.delete(cuenta_por_cobrar)

            # Se confirma la eliminación en la base de datos
            db.session.commit()

            return {"mensaje" : "cuenta y pagos eliminados"}, 200
        except Exception as e:
            # Se revierte la transacción en caso de error
            db.session.rollback()
            raise e
        