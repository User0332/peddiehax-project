import secrets
from flask import jsonify
from webpy import App
from propelauth_flask import init_auth, current_user
from propelauth_flask.user import LoggedInUser
import sys
import os

DEBUG = True

current_user: LoggedInUser

sys.path.append(
	os.path.join(
		os.getcwd(),
		"glblib"
	)
)

app = App(__name__, template_folder="html")

db = app.sqlalchemy.init("sqlite:///db/database.db")

def init_propelauth(app: App):
	app.secret_key = secrets.token_urlsafe(16)

	with open("instance/PROPELAUTH_INFO", 'r') as f:
		app.config["PROPELAUTH_URL"] = f.readline().strip()	
		app.config["PROPELAUTH_KEY"] = f.readline().strip()

	return init_auth(app.config["PROPELAUTH_URL"], app.config["PROPELAUTH_KEY"], debug_mode=DEBUG)

sys.path.insert(0, '.')

auth = init_propelauth(app)

def webpy_setup(app: App):
	app.debug = DEBUG

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
	added_at = db.Column(db.DateTime, nullable=False)
	parent_journey = db.Column(db.String, nullable=False)

# WebPy design requires that all specially-decorated functions
# (such as the following with require_user) be defined in app.py rather that root/

@app.route("/api/getself")
@auth.require_user
def getself():
	user = db.session.execute(
		db.select(User).where(User.id == current_user.user_id)
	).scalar()

	if not user: return jsonify(None)

	return jsonify(
		{
			"username": user.username,
			"id": user.id,
			"journeys": user.journeys.split(',')
		}
	)

@app.route("/api/whoami")
@auth.require_user
def whoami():
	return f"{current_user.user.first_name} {current_user.user.last_name}"