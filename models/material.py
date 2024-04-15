from app import db, ma

class Material(db.Model):
    __tablename__ = 'materiales'

    codigo_material = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(255), nullable = False)
    precio_unitario = db.Column(db.Float, nullable = False)
    existencias = db.Column(db.Integer, nullable = False)

    def __init__(self, descripcion, precio_unitario, existencias):
        self.descripcion = descripcion
        self.precio_unitario = precio_unitario
        self.existencias = existencias

    def __repr__ (self):
        return '<Material %r>' % self.descripcion
    
#Material Schema
class MaterialSchema(ma.Schema):
    class Meta: #Fields Permitidos para mostrar
        fields = ('codigo_material','descripcion', 'precio_unitario', 'existencias')