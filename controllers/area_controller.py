from models.area import Area
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
            
