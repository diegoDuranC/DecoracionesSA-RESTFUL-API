from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config.config import Config
from flask_cors import CORS
#from flask_swagger_ui import get_swaggerui_blueprint

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)

    CORS(app, resources={r"/*": {"origins": "*"}})


    with app.app_context():
        # Importar las rutas aquí evita la importacion circular
        from routes.material_routes import material_bp
        from routes.cliente_routes import cliente_bp
        from routes.empleado_routes import empleado_bp
        from routes.area_routes import area_bp
        from routes.cargo_routes import cargo_bp
        from routes.banco_routes import banco_bp
        from routes.proveedor_routes import proveedor_bp
        from routes.proyecto_routes import proyecto_bp
        from routes.requisicion_routes import requisicion_bp
        from routes.orden_de_compra_routes import orden_compra_bp
        from routes.recibos_routes import recibo_bp
        from routes.nota_de_entrega_routes import nota_entrega_bp
        from routes.factura_orden_routes import factura_orden_bp
        from routes.deposito_routes import deposito_bp
        from routes.cuentas_por_cobrar_routes import cuenta_cobrar_bp
        from routes.transaccion_inventario_routes import transaccion_inventario_bp

        app.register_blueprint(material_bp)
        app.register_blueprint(cliente_bp)
        app.register_blueprint(empleado_bp)
        app.register_blueprint(area_bp)
        app.register_blueprint(cargo_bp)
        app.register_blueprint(banco_bp)
        app.register_blueprint(proveedor_bp)
        app.register_blueprint(proyecto_bp)
        app.register_blueprint(requisicion_bp)
        app.register_blueprint(orden_compra_bp)
        app.register_blueprint(recibo_bp)
        app.register_blueprint(nota_entrega_bp)
        app.register_blueprint(factura_orden_bp)
        app.register_blueprint(deposito_bp)
        app.register_blueprint(cuenta_cobrar_bp)
        app.register_blueprint(transaccion_inventario_bp)
        #app.register_blueprint(swaggerui_blueprint)
    
    return app

def create_tables(app):
    
    with app.app_context():

        #MODELOS
                
        from models.material.material import Material

        # rrhh
        from models.rrhh.area import Area
        from models.rrhh.cargo import Cargo
        from models.rrhh.empleado import Empleado
        
        # compras
        from models.compras.orden_de_compra import OrdenDeCompra
        from models.compras.factura_orden import FacturaOrdenCompra
        from models.compras.detalle_orden import DetalleOrdenCompra
        from models.compras.nota_de_entrega import NotaDeEntrega
        from models.compras.material_recibido import MaterialRecibido
        from models.compras.entrega_pendiente import EntregaPendiente
        from models.compras.detalle_material_pendiente import DetalleMaterialPendiente
        
        # models
        from models.proveedor import Proveedor          
        from models.proyecto import Proyecto

        # requisicion
        from models.requisicion.requisicion import Requisicion
        from models.requisicion.detalle_materiales import DetalleMaterialRequisicion
        
        # cliente
        from models.cliente.cliente import Cliente
        from models.cliente.cuenta_cobrar import CuentaPorCobrar
        from models.cliente.plan_pago_cliente import PlanPagoCliente
        from models.cliente.factura_cliente import FacturaCliente
        from models.cliente.detalle_factura import DetalleFactura
        from models.cliente.recibo import Recibo
        
        # banco
        from models.banco.banco import Banco
        from models.banco.deposito import Deposito

        #transaccion inventario
        from models.material.transacciones_inventario import TransaccionInventario
        
        db.create_all()
    # with app.app_context():
    #     db.create_all()