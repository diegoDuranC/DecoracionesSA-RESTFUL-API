from multiprocessing import context
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config.config import Config
from flask_cors import CORS


db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)

    CORS(app)

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
    
    return app

def create_tables(app):
    
    #MODELOS
    #rrhh
    from models.rrhh.area import Area
    from models.rrhh.cargo import Cargo
    from models.rrhh.empleado import Empleado
    
    #compras
    from models.compras.orden_de_compra import OrdenDeCompra
    from models.compras.factura_orden import FacturaOrdenCompra
    from models.compras.nota_entrega import NotaDeEntrega
    from models.compras.detalle_orden import DetalleOrdenCompra
    
    #models
    from models.proveedor import Proveedor          
    from models.proyecto import Proyecto
    
    #material
    from models.material.material import Material
    
    #requisicion
    from models.requisicion.requisicion import Requisicion
    from models.requisicion.detalle_materiales import DetalleMaterialRequisicion
    
    #cliente
    from models.cliente.cliente import Cliente
    from models.cliente.cuenta_cobrar import CuentaPorCobrar
    from models.cliente.plan_pago_cliente import PlanPagoCliente
    from models.cliente.factura_cliente import FacturaCliente
    from models.cliente.detalle_factura import DetalleFactura
    from models.cliente.recibo import Recibo
    
    #banco
    from models.banco.banco import Banco
    from models.banco.deposito import Deposito
    
    with app.app_context():
        db.create_all()