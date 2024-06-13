from app import db, ma

class Cargo(db.Model):
    __tablename__ = "cargos"

    id_cargo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_cargo = db.Column(db.String(20), nullable=False)
    cargo = db.Column(db.String(50), nullable=False)

    empleado = db.relationship('Empleado', back_populates='cargo', uselist=False)

    def __init__(self, cargo, cod_cargo):
        self.cargo = cargo
        self.cod_cargo = cod_cargo

class CargoSchema(ma.Schema):
    class Meta():
        fields = ('id_cargo', 'cargo', 'cod_cargo')