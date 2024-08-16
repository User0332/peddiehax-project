from webpy import App
import flask_sqlalchemy as sqlalchemy
import sys
import os

sys.path.append(
	os.path.join(
		os.getcwd(),
		"glblib"
	)
)

app = App(__name__, template_folder="html")

db = app.sqlalchemy.init("sqlite:///./db/local.db")

def webpy_setup(app: App):
	app.debug = True

class User(db.Model):
	id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
	username = db.Column(db.String, unique=True, nullable=False)
	journeys = db.Column(db.String) # comma-separated list of ids

class Journey(db.Model):
	id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
	name = db.Column(db.String, nullable=False)
	entries = db.Column(db.String) # comma-separated list of ids
	parent_user = db.Column(db.String, nullable=False)

class TripEntry(db.Model):
	id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
	name = db.Column(db.String, nullable=False)
	geo_location = db.Column(db.String, nullable=False)
	people = db.Column(db.String, nullable=False)
	description = db.Column(db.String, nullable=False)
	rating = db.Column(db.Integer, nullable=False)
	parent_journey = db.Column(db.String, nullable=False)