from app import db, ma
from .cargo import Cargo
from .area import Area

class Empleado(db.Model):
    __tablename__ = 'empleados'
    
    codigo_empleado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ci_empleado = db.Column(db.String(7), unique=True, nullable=False)
    nombre_empleado = db.Column(db.String(80), nullable=False)
    apellido_empleado = db.Column(db.String(80), nullable=False)
    telefono_empleado = db.Column(db.String(8), unique=True)
    estado = db.Column(db.String(20), nullable=False)
    fecha_contratacion = db.Column(db.Date(), nullable=False)
    fecha_despido = db.Column(db.Date(), nullable=True)
    
    #RELACIONES
    cargo = db.Column(db.Integer, db.ForeignKey(Cargo.id_cargo))
    area = db.Column(db.Integer, db.ForeignKey(Area.id_area))
    jefe_id = db.Column(db.Integer, db.ForeignKey(codigo_empleado), nullable=True)

    def __init__(
                    self,
                    ci_empleado, 
                    nombre_empleado,
                    apellido_empleado,
                    telefono_empleado,
                    estado,
                    fecha_contratacion,
                    cargo,
                    area,
                    jefe_id = None
                ):
        
        self.ci_empleado = ci_empleado
        self.nombre_empleado = nombre_empleado
        self.apellido_empleado = apellido_empleado
        self.telefono_empleado = telefono_empleado
        self.estado = estado
        self.cargo = cargo
        self.area = area
        self.jefe_id = jefe_id
        self.fecha_contratacion = fecha_contratacion
    
    def __repr__(self):
        return f"Empleado(codigo_empleado={self.codigo_empleado}, nombre_empleado='{self.nombre_empleado}', apellido_empleado='{self.apellido_empleado}', telefono_empleado='{self.telefono_empleado}', cargo_empleado='{self.cargo_empleado}', area_empleado='{self.area_empleado}')"

class EmpleadoSchema(ma.Schema):
    class Meta:
        fields = (
            'codigo_empleado', 'ci_empleado', 'nombre_empleado', 'apellido_empleado', 
            'telefono_empleado', 'estado', 'fecha_contratacion','cargo', 'area', 'jefe_id'
        )


