from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates 

# Create Flask app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object("app.config.Config")
db = SQLAlchemy(app)

# TODO: Move the data model into its own file
class Target(db.Model):
    __tablename__ = "targets"

    # TODO: add all in
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=True)
    latitude = db.Column(db.Numeric(precision=8, scale=6), nullable=False)
    longitude = db.Column(db.Numeric(precision=9, scale=6), nullable=False)
    elevation = db.Column(db.Numeric(precision=6, scale=2), nullable=True)

    def __init__(self, name, latitude, longitude, elevation):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        super(Target, self).__init__()

@app.route('/')
def hello_world():
    return jsonify(hello='GIS world')

@app.route('/new-target', methods=['POST'])
def target_create():
    data = request.get_json()
    name = data['name']
    latitude = data['latitude']
    longitude = data['longitude']
    elevation = data['elevation']
    target = Target(name, latitude, longitude, elevation)

    try:
        db.session.add(target)
        db.session.commit()
        return jsonify(msg='New target is created', target_id=target.id), 200

    except AssertionError as exception_message:
        return jsonify(msg='Error: {}. '.formate(exception_message)), 400

# TODO: Validation seem not working, need to fix
@validates('latitude')
def validate_latitude(self, key, latitude):
    if not latitude:
        raise AssertionError('No latitude provided')

    if latitude > 90 or latitude < -90:
        raise AssertionError('Latitude must be between -90 and 90')

    return latitude  @validates('longitude')

@validates('longitude')
def validate_latitude(self, key, longitude):
    if not longitude:
        raise AssertionError('No longitude provided')

    if longitude > 180 or longitude < -180:
        raise AssertionError('Latitude must be between -90 and 90')

    return longitude
