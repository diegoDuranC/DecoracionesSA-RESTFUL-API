from app import db, ma
from sqlalchemy import Column, Integer, Float, ForeignKey
from marshmallow import fields
from models.material.material import MaterialSchema

class MaterialRecibido(db.Model):
    __tablename__ = "materiales_recibidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cantidad_recibida = Column(Float)
    
    id_material = Column(Integer, ForeignKey('materiales.ID_material'))
    material = db.relationship('Material', back_populates='materiales_recibidos')
    
    # Relaciones
    nro_nota = Column(Integer, ForeignKey('notas_de_entrega.nro_nota'))
    nota_de_entrega = db.relationship('NotaDeEntrega', back_populates='materiales_recibidos')

    transaccion = db.relationship('TransaccionInventario', back_populates='material_recibido', uselist=False)

    def __init__(self, cantidad_recibida, nro_nota, id_material):
        self.id_material = id_material
        self.cantidad_recibida = cantidad_recibida
        self.nro_nota = nro_nota

class MaterialRecibidoSchema(ma.Schema):
    material = fields.Nested(MaterialSchema, only=('descripcion',))
    class Meta:
        model = MaterialRecibido
        fields = ("id", "ID_material", "cantidad_recibida", "nro_nota", "material")

