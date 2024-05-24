from app import db, ma

class Cargo(db.Model):
    __tablename__ = "cargos"

    id_cargo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cargo = db.Column(db.String(50), nullable=False, unique=True)
    empleado = db.relationship('Empleado', back_populates='cargo', uselist=False)

    def __init__(self, cargo):
        self.cargo = cargo

class CargoSchema(ma.Schema):
    class Meta():
        fields = ('id_cargo', 'cargo')