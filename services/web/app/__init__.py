from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from sqlalchemy import func
from sqlalchemy.orm import validates
# from elasticsearch import Elasticsearch

# Create Flask app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object("app.config.Config")
db = SQLAlchemy(app)
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# TODO: Move the data model into models.py
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

# TODO: Move routes into routes.py

# A default home page
@app.route('/')
def hello_world():
    return jsonify(hello='GIS world')

# Create new target
@app.route('/targets', methods=['POST'])
def target_create():
    data = request.get_json()
    name = data['name']
    latitude = data['latitude']
    longitude = data['longitude']
    geomerty = data['geomerty']
    elevation = data['elevation']
    image = None
    image_timestamp = None

    target = Target(name, latitude, longitude, geomerty, elevation, image, image_timestamp)
    try:
        db.session.add(target)
        db.session.commit()
        return jsonify(message='New target is created', target_id=target.id), 200

    except AssertionError as exception_message:
        return jsonify(message='Error: {}. '.formate(exception_message)), 400

# Add image and datetime to an existing target
@app.route('/targets/<id>', methods=['PATCH'])
def target_update(id):
    data = request.get_json()
    target = Target.query.get(id)

    target.image = data['image']
    target.image_timestamp = data['image_timestamp']

    try:
        db.session.commit()
        return jsonify(message='Image is saved', target_id=target.id), 200

    except AssertionError as exception_message:
        return jsonify(message='Error: {}. '.formate(exception_message)), 400

@app.route('/targets/search', methods=['GET', 'POST'])
def search():
	data = request.get_json()
	xmin = data['xmin']
	ymin = data['ymin']
	xmax = data['xmax']
	ymax = data['ymax']
	result = []

	# TODO: Need to test if this query works
	targets = Target.query.filter(func.ST_Contains(func.ST_Transform(func.ST_MakeEnvelope(xmin, ymin, xmax, ymax, 4326), 3857), Target.geomerty)).all()

	for target in targets:
		result.append()

	return jsonify(result)

	# TODO: Elasticsearch provides Geo-bounding box search query.
	# 		The Code below does not work at the moment, need to fix.

    # while True:
    # 	try:
    #     	es.search(index="")
    #     	break
    # 	except (
    #     	elasticsearch.exceptions.ConnectionError,
    #     	elasticsearch.exceptions.TransportError
    # 	):
    #     	time.sleep(1)

    # keyword = request.get_json()['box']

    # body = {
    #   "fields": 'geomerty',
    #   "query": {
    #     "bool": {
    #       "must": {
    #         "match_all": {}
    #       },
    #       "filter": {
    #         "geo_bounding_box": {
    #           "pin.location": {
    #             "wkt": keyword
    #           }
    #         }
    #       }
    #     }
    #   }
    # }

    # res = es.search(index="contents", doc_type="title", body=body)

    # return jsonify(res['hits']['hits'])
    

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
