from app import db, ma
from marshmallow import fields
from models.rrhh.empleado import EmpleadoSchema

class Departamento(db.Model):
    __tablename__ = "departamentos"

    ID_departamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    departamento = db.Column(db.String(50), nullable=False, unique=True)
    empleados = db.relationship('Empleado', back_populates='departamento')

    def __init__(self, departamento):
        self.departamento = departamento

class DepartamentoSchema(ma.Schema):
    empleados = fields.List(fields.Nested(EmpleadoSchema), exclude=('departamento',))
    class Meta:
        fields = ('ID_departamento', 'departamento', 'empleados')