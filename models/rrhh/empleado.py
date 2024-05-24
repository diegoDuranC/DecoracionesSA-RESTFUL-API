from app import db, ma
from .cargo import Cargo
from .area import Area
from .area import AreaSchema
from .cargo import CargoSchema

class Empleado(db.Model):
    __tablename__ = 'empleados'
    
    codigo_empleado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ci_empleado = db.Column(db.String(7), unique=True, nullable=False)
    nombre_empleado = db.Column(db.String(80), nullable=False)
    apellido_empleado = db.Column(db.String(80), nullable=False)
    telefono_empleado = db.Column(db.String(8), unique=True)
    fecha_contratacion = db.Column(db.Date(), nullable=False)
    fecha_despido = db.Column(db.Date(), nullable=True)
    jefe_id = db.Column(db.Integer, db.ForeignKey(codigo_empleado), nullable=True)
    cargo_id = db.Column(db.Integer, db.ForeignKey(Cargo.id_cargo))
    area_id = db.Column(db.Integer, db.ForeignKey(Area.id_area))

    #RELACIONES
    #JEFE Relación recursiva: Un empleado tiene un jefe   
    jefe = db.relationship('Empleado', remote_side=[codigo_empleado], back_populates='subordinados')

    #Relación recursiva inversa: Un jefe tiene subordinados
    subordinados = db.relationship('Empleado', back_populates='jefe')
  
    #Relación uno a uno con Area
    area = db.relationship('Area', back_populates='empleado')

    # Relación uno a uno con Cargo
    cargo = db.relationship('Cargo', back_populates='empleado')

    # Relación con deposito
    depositos = db.relationship('Deposito', back_populates='empleado')

    #Relacion muchos a uno con proyecto
    proyectos = db.relationship('Proyecto', back_populates='encargado')

    #Relacion con recibos
    recibos = db.relationship('Recibo', back_populates='empleado')

    def __init__(
                    self,
                    ci_empleado, 
                    nombre_empleado,
                    apellido_empleado,
                    telefono_empleado,
                    fecha_contratacion,
                    fecha_despido,
                    cargo_id,
                    area_id,
                    jefe_id = None
                ):
        
        self.ci_empleado = ci_empleado
        self.nombre_empleado = nombre_empleado
        self.apellido_empleado = apellido_empleado
        self.telefono_empleado = telefono_empleado
        self.cargo_id = cargo_id
        self.area_id = area_id
        self.jefe_id = jefe_id
        self.fecha_contratacion = fecha_contratacion
        self.fecha_despido = fecha_despido
    
    def __repr__(self):
        return f"Empleado(codigo_empleado={self.codigo_empleado}, nombre_empleado='{self.nombre_empleado}', apellido_empleado='{self.apellido_empleado}', telefono_empleado='{self.telefono_empleado}', cargo_empleado='{self.cargo_empleado}', area_empleado='{self.area_empleado}')"

class EmpleadoSchema(ma.Schema):

    cargo = ma.Nested(CargoSchema)
    area = ma.Nested(AreaSchema)
    jefe = ma.Nested('self', only=('codigo_empleado', 'nombre_empleado', 'apellido_empleado'))

    class Meta:
        
        fields = (
            'codigo_empleado', 'ci_empleado', 'nombre_empleado', 'apellido_empleado', 
            'telefono_empleado', 'fecha_contratacion', 'fecha_despido', 'cargo', 'area', 'jefe'
        )
        
class EmpleadoRequisicionSchema(ma.Schema):
    model = Empleado
    class Meta():
        fields = ('nombre_empleado', 'apellido_empleado')

