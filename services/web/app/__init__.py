from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

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
    name = db.Column(db.String(255), unique=False)
    latitude = db.Column(db.Float(8), nullable=False)

    def __init__(self, name, latitude):
        self.name = name
        self.latitude = latitude
        super(Target, self).__init__()

@app.route('/')
def hello_world():
    return jsonify(hello='world')
