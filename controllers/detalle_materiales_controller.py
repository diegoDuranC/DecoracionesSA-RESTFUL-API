from app import db
from flask import request
from models.requisicion.detalle_materiales import DetalleMaterialRequisicion
from models.material.material import Material

class DetalleMaterialesController():

    def get_detalles(self):
        detalles = DetalleMaterialRequisicion.query.all()
        return detalles
    
    def get_detalles_requisicion(self, nro_requisicion):     
        detalles = DetalleMaterialRequisicion.query.filter_by(nro_requisicion=nro_requisicion).all()
        return detalles
    
    def actualizar_detalle(self, id_detalle, nro_requisicion, codigo_material):

        detalle = DetalleMaterialRequisicion.query.get_or_404((id_detalle, nro_requisicion, codigo_material))

        if 'cantidad_solicitada' in request.json:
            cantidad_solicitada_anterior = detalle.cantidad_solicitada       
            cantidad_solicitada_peticion = request.json['cantidad_solicitada']

            material = Material.query.get(detalle.codigo_material)
            
            if cantidad_solicitada_anterior != cantidad_solicitada_peticion:
                diferencia = cantidad_solicitada_peticion - cantidad_solicitada_anterior

                if cantidad_solicitada_anterior < cantidad_solicitada_peticion:
                    if material.existencias < diferencia:
                        return {"error": f"¡No hay suficiente stock disponible de {material.descripcion}!"}
                    #DISMINUIMOS STOCK     
                    material.existencias -= diferencia
                else:
                    material.existencias += abs(diferencia) 

                detalle.cantidad_solicitada = cantidad_solicitada_peticion
            else:
                return {"Ingrese un monto valido"}
                      
        if 'nro_requisicion' in request.json: detalle.nro_requisicion = request.json['encargado_proyecto']
        if 'codigo_material' in request.json: detalle.codigo_material = request.json['codigo_material']

        db.session.commit()

        return detalle