from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config.config import Config

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    ma.init_app(app)
    db.init_app(app)

    with app.app_context():
        # Importing routes here avoids a circular reference
        from routes.material_routes import material_bp
        from routes.cliente_routes import cliente_bp
        from routes.empleado_routes import empleado_bp
        from routes.area_routes import area_bp
        from routes.cargo_routes import cargo_bp

        db.create_all()

        app.register_blueprint(material_bp)
        app.register_blueprint(cliente_bp)
        app.register_blueprint(empleado_bp)
        app.register_blueprint(area_bp)
        app.register_blueprint(cargo_bp)

    return app