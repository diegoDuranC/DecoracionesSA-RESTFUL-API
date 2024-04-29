from app import db, ma

class Banco(db.Model):
    __tablename__ = "bancos"

    nro_banco = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(80), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    ciudad = db.Column(db.String(30), nullable=False)

    def __init__(self, nombre, direccion, ciudad):
        self.nombre = nombre
        self.direccion = direccion
        self.ciudad = ciudad

    def __repr__(self):
        return f'Banco {self.nombre} en {self.ciudad}' 
    
class BancoSchema(ma.Schema):
    class Meta:
        fields = ('nro_banco', 'nombre', 'direccion', 'ciudad')