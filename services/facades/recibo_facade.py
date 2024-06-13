from decimal import Decimal
from utils.date_utils import format_date
from datetime import datetime
from app import db

from models.cliente.cliente import Cliente
from models.cliente.cuenta_cobrar import CuentaPorCobrar
from models.banco.deposito import Deposito
from models.cliente.factura_cliente import FacturaCliente
from models.cliente.recibo import Recibo, ReciboSchema
from models.proyecto import Proyecto

from decimal import Decimal

class ReciboFacade():
    
    def __init__(self):

        self.recibo_schema = ReciboSchema()
        self.recibo_schemas = ReciboSchema(many=True)

    def crear_recibo(self, request_data):

        '''
            Crea un recibo en base al siguiente json
            {
                "nro_cuenta" : int() -> nro_cuenta a la cual se le hara el recibo,
                "monto" : float(), decimal() -> monto a pagar,
            }
        '''

        nro_cuenta = request_data.get('nro_cuenta')
        cuenta = CuentaPorCobrar.query.get(nro_cuenta)

        if not cuenta:
            return {"Error" : "Cuenta no encontrada"}
        
        factura = FacturaCliente.query.get(cuenta.nro_factura)

        if factura is None:
            return {"Error" : "No hay factura"}

        nro_proyecto = factura.proyecto_id

        proyecto = Proyecto.query.get(nro_proyecto)
        cliente = Cliente.query.get(cuenta.id_cliente)
        
        ci_cliente = cliente.ci_cliente
        monto = Decimal(request_data.get('monto'))
        empleado_id = proyecto.encargado_proyecto
        
        #GENERAR EL RECIBO
        nuevo_recibo = Recibo(
            ci_cliente = ci_cliente,
            monto = monto,
            cuenta_por_cobrar_id = nro_cuenta,
            empleado_id = empleado_id,
            deposito_id = None,
            numero_proyecto=nro_proyecto
        )

        db.session.add(nuevo_recibo)

        #Disminuir la deuda
        cuenta.saldo -= monto
        if cuenta.saldo < 0:
            return {"Error" : "El saldo es 0, no puede ser negativo"}    
        try:
            db.session.commit()

        except Exception as e:

            db.session.rollback()
            return {"Error": str(e)}

        return self.recibo_schema.dump(nuevo_recibo)

    def obtener_recibos(self):
        consulta = Recibo.query.all()
        return self.recibo_schemas.dump(consulta)

    def obtener_recibos_por_fecha(self, fecha_inicio, fecha_fin):
        '''
            Retorna una lista con instancias de recibos en un intervalo de fechas
        '''
        fecha_inicio = format_date(fecha_inicio)
        fecha_fin = format_date(fecha_fin)

        # Convertir las fechas de cadena a objeto datetime
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')

        except ValueError:
            return {"Error": "Formato de fecha inválido. Utilice YYYY-MM-DD."}
        
        query = Recibo.query.filter(Recibo.fecha.between(fecha_inicio_dt,fecha_fin_dt)).all()

        if not query:
            return {"Error" : "No se encontraron recibos"}

        return  self.recibo_schemas.dump(query)
    
    def obtener_recibos_ci_cliente(self, ci_cliente):

        consulta = Recibo.query.filter_by(ci_cliente=ci_cliente)

        if not consulta:
            return {"Error" : "El cliente no tiene recibos"}

        return self.recibo_schemas.dump(consulta)
    
    def obtener_recibos_del_dia(self):

        fecha_incio = datetime.now().strftime("%Y-%m-%d")
        fecha_fin = datetime.now().strftime("%Y-%m-%d")

        recibos = self.obtener_recibos_por_fecha(fecha_inicio=fecha_incio, fecha_fin=fecha_fin)

        if not recibos:
            return {"Error" : "No hay recibos hoy"}
        
        return self.recibo_schemas.dump(recibos)
    
    def obtener_recibos_sin_deposito_monto_total(self, fecha_inicio, fecha_fin):
        '''
            Retorna los recibos en un intervalo de fechas que no están asociados a un depósito y la suma total de esos recibos.
        
            :param fecha_inicio: Fecha de inicio del intervalo.
            :param fecha_fin: Fecha de fin del intervalo.
            :return: Un diccionario con los recibos y el monto total.
        '''
        recibos = Recibo.query.filter(
            Recibo.fecha.between(fecha_inicio, fecha_fin),
            Recibo.deposito_id == None
        ).all()

        if not recibos:
            return {"Error": "No hay recibos por ahora"}

        monto_total = sum(recibo.monto for recibo in recibos)

        return {
            "recibos": self.recibo_schemas.dump(recibos),
            "monto_total": str(monto_total)  # Convertir Decimal a string para evitar problemas de serialización
        }
