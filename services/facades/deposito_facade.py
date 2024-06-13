from flask import request
from sqlalchemy.exc import SQLAlchemyError
from app import db
from models.banco.deposito import Deposito, DepositoSchema, FormaPago, DepositoRecibosSchema
from models.cliente.recibo import Recibo
from datetime import datetime
from decimal import Decimal
from .recibo_facade import ReciboFacade

class DepositoFacade:
    def __init__(self):
        self.deposito_schema = DepositoSchema()
        self.depositos_schema = DepositoSchema(many=True)
        self.recibo_facade = ReciboFacade()
        self.deposito_recibo_schema = DepositoRecibosSchema()
        self.deposito_recibo_schemas = DepositoRecibosSchema(many=True)

    def get_depositos(self):
        consulta = Deposito.query.all()
        return self.deposito_recibo_schemas.dump(consulta)

    def crear_deposito(self, cuenta, fecha, monto, banco_id, forma_pago):
        try:
            nuevo_deposito = Deposito(
                cuenta=cuenta,
                fecha=fecha,
                monto=monto,
                banco_id=banco_id,
                forma_pago=FormaPago[forma_pago]  # Asegura que el valor de forma_pago sea una opción válida
            )

            db.session.add(nuevo_deposito)
            db.session.commit()
            
            return self.deposito_schema.dump(nuevo_deposito)
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"Error": str(e)}
        
    def crear_deposito_con_recibos_del_dia(self, cuenta, banco_id, forma_pago):

        #Puedes pasar parametros del dia
        # fecha_inicio = "YYYY-mm-dd"
        # fecha_fin = "YYYY-mm-dd"

        fecha_inicio_req = request.args.get('fecha_inicio')
        fecha_fin_req = request.args.get("fecha_fin")

        try:
            if fecha_inicio_req is None and fecha_fin_req is None:

                fecha_incio = datetime.now().strftime("%Y-%m-%d")
                fecha_fin = datetime.now().strftime("%Y-%m-%d")

                recibos = self.recibo_facade.obtener_recibos_por_fecha(fecha_inicio=fecha_incio, fecha_fin=fecha_fin, deposito_id=None)
                
                if "Error" in recibos:
                    return recibos

                monto_total = sum(Decimal(recibo['monto']) for recibo in recibos)
                fecha = datetime.now().strftime("%Y-%m-%d")

                nuevo_deposito = Deposito(
                    cuenta=cuenta,
                    fecha=fecha,
                    monto=monto_total,
                    banco_id=banco_id,
                    forma_pago=FormaPago[forma_pago]  # Asegura que el valor de forma_pago sea una opción válida
                )

                db.session.add(nuevo_deposito)
                db.session.flush()  # Obtener el ID del nuevo depósito para asociarlo a los recibos

                for recibo in recibos:
                    recibo_obj = Recibo.query.get(recibo['nro_recibo'])
                    recibo_obj.deposito_id = nuevo_deposito.nro_deposito
                    db.session.add(recibo_obj)

                db.session.commit()
                return self.deposito_schema.dump(nuevo_deposito)
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"Error": str(e)}
    
    '''
        Generar un deposito con una lista de recibos
    '''
    def crear_deposito_recibos(self, recibos, cuenta, banco_id, forma_pago):
        
        try:
            monto_total = sum(Decimal(recibo['monto']) for recibo in recibos)
            fecha = datetime.now().strftime("%Y-%m-%d")

            nuevo_deposito = Deposito(
                    cuenta=cuenta,
                    fecha=fecha,
                    monto=monto_total,
                    banco_id=banco_id,
                    forma_pago=FormaPago[forma_pago]  # Asegura que el valor de forma_pago sea una opción válida
            )
        
            db.session.add(nuevo_deposito)
            db.session.flush()

            for recibo_data in recibos:
                recibo_id = recibo_data['nro_recibo'] 
                recibo = Recibo.query.get(recibo_id)
                if recibo:
                    recibo.deposito_id = nuevo_deposito.nro_deposito
                    db.session.add(recibo)

            db.session.commit()

            return self.deposito_recibo_schema.dump(nuevo_deposito)
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"Error": str(e)}