from models.rrhh.area import Area
from app import db
from flask import request

class AreaController():

    def create_area(self):
            area = request.json['area']

            if area is None :
                return None
            
            nueva_area = Area(area)

            db.session.add(nueva_area)
            db.session.commit()

            return nueva_area
    
    def get_areas(self):
        return Area.query.all()
    
    def get_area(self, area_id):
        area = Area.query.get(area_id)

        return area

    def update_area(self, area_id):
        area = Area.query.get(area_id)

        if 'area' in request.json:
            area.area = request.json['area']

        return area
    
    def delete_area(self, area_id):
         area = Area.query.get(area_id)

         db.session.delete(area)
         db.session.commit()

         return area
