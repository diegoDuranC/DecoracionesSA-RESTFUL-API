from app import db, ma
from sqlalchemy import Column, Integer, Float, ForeignKey
from marshmallow import fields
from .nota_de_entrega import NotaDeEntrega
from models.material.material import MaterialSchema

class MaterialRecibido(db.Model):
    __tablename__ = "materiales_recibidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cantidad_recibida = Column(Float)
    
    cod_material = Column(Integer, ForeignKey('materiales.codigo_material'))
    material = db.relationship('Material', back_populates='materiales_recibidos')
    
    # Relaciones
    #nota de entrega
    nro_nota = Column(Integer, ForeignKey('notas_de_entrega.nro_nota'))
    nota_de_entrega = db.relationship('NotaDeEntrega', back_populates='materiales_recibidos')

    #Entregas pendientes
    id_entrega_pendiente = Column(Integer, ForeignKey('entregas_pendientes.id_entrega_pendiente'))
    entrega_pendiente = db.relationship('EntregaPendiente', back_populates='materiales_recibidos')

    def __init__(self, cod_material, cantidad_recibida, nro_nota):
        self.cod_material = cod_material
        self.cantidad_recibida = cantidad_recibida
        self.nro_nota = nro_nota

class MaterialRecibidoSchema(ma.Schema):
    material = fields.Nested(MaterialSchema, only=('descripcion',))
    class Meta:
        model = MaterialRecibido
        fields = ("cod_material", "cantidad_recibida", "nro_nota", "material")

