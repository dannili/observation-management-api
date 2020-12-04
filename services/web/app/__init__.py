from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from sqlalchemy import func
from sqlalchemy.orm import validates
from elasticsearch import Elasticsearch

# Create Flask app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object("app.config.Config")
db = SQLAlchemy(app)
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

from .models import Target

# A default home route
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

	# TODO: Need to test if this query returns correct results
	targets = Target.query.filter(func.ST_Contains(func.ST_Transform(func.ST_MakeEnvelope(xmin, ymin, xmax, ymax, 4326), 3857), Target.geomerty)).all()
	result = [target for target in targets]

	return jsonify(result)

	# TODO: Elasticsearch also provides Geo-bounding box search query.
	# 		The Code below is WIP.

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
    

# TODO: Validation seem not working, need to fix. Also move to its own file
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
