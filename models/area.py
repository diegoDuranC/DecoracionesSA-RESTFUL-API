from app import db, ma

class Area(db.Model):
    __tablename__ = "areas"

    id_area = db.Column(db.Integer, primary_key=True, autoincrement=True)
    area = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, area):
        self.area = area

class AreaSchema(ma.Schema):
    class Meta:
        fields = ('id_area', 'area')