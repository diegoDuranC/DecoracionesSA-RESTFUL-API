from app import db, ma
from marshmallow import fields
from .cargo import CargoSchema
'''
    Agregar Cargo
'''

class Empleado(db.Model):
    __tablename__ = 'empleados'
    
    ID_empleado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_empleado = db.Column(db.String(20), nullable=False, unique=True)
    ci = db.Column(db.String(7), unique=True, nullable=False)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    telefono = db.Column(db.String(8), unique=True)
    departamento_id = db.Column(db.Integer, db.ForeignKey("departamentos.ID_departamento"))
  
    #Relación uno a uno con Area
    departamento = db.relationship('Departamento', back_populates='empleados')

    cargo_id = db.Column(db.Integer, db.ForeignKey("cargos.id_cargo"))
    cargo = db.relationship('Cargo', back_populates='empleado', uselist=False)

    # Relación con deposito
    depositos = db.relationship('Deposito', back_populates='empleado')

    #Relacion muchos a uno con proyecto
    proyectos = db.relationship('Proyecto', back_populates='encargado')

    #Relacion con recibos
    recibos = db.relationship('Recibo', back_populates='empleado')

    def __init__(
                    self,
                    cod_empleado,
                    ci, 
                    nombre,
                    apellido,
                    telefono,
                    cargo_id,
                    departamento_id,
                ):
        
        self.cod_empleado = cod_empleado
        self.ci = ci
        self.nombre = nombre.upper()
        self.apellido = apellido.upper()
        self.telefono = telefono
        self.cargo_id = cargo_id
        self.departamento_id = departamento_id
    
    def __repr__(self):
        return f"Empleado(codigo_empleado={self.cod_empleado}, nombre_empleado='{self.nombre}', apellido_empleado='{self.apellido}', telefono_empleado='{self.telefono}', cargo_empleado='{self.cargo}', departamento_empleado='{self.departamento_id}')"

class EmpleadoSchema(ma.Schema):
    cargo = fields.Nested(CargoSchema)
    class Meta: 
        fields = (
            'ID_empleado', 'cod_empleado', 'ci', 'nombre', 'apellido', 
            'telefono', 'cargo', 'departamento_id'
        )
        
class EmpleadoRequisicionSchema(ma.Schema):
    model = Empleado
    cargo = fields.Nested(CargoSchema)
    class Meta():
        fields = ('nombre', 'apellido', 'cargo')

