"""Data models."""
from . import db
from geoalchemy2 import Geometry

class Target(db.Model):
    __tablename__ = "targets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=True)
    latitude = db.Column(db.Numeric(precision=8, scale=6), nullable=False)
    longitude = db.Column(db.Numeric(precision=9, scale=6), nullable=False)
    geomerty = db.Column(Geometry(geometry_type='POINT'))
    elevation = db.Column(db.Numeric(precision=6, scale=2), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    image_timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, name, latitude, longitude, geomerty, elevation, image, image_timestamp):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.geomerty = geomerty
        self.elevation = elevation
        self.image = image
        self.image_timestamp = image_timestamp
        super(Target, self).__init__()