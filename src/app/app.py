import datetime
import secrets
import base64
import googlemaps
from flask import Response, jsonify, request
from webpy import App
from propelauth_flask import init_auth, current_user
from propelauth_flask.user import LoggedInUser
import genid
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

app.config["GMAPS_API_KEY"] = open("instance/API_KEY", 'r').read().strip()

maps = googlemaps.Client(app.config["GMAPS_API_KEY"])

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
	journeys = db.Column(db.String, nullable=False, default="") # comma-separated list of ids

	@property
	def journey_list(self):
		return list(
			filter(None, self.journeys.split(','))
		)

class Journey(db.Model):
	id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
	name = db.Column(db.String, nullable=False)
	entries = db.Column(db.String, nullable=False, default="") # comma-separated list of ids
	owner_id = db.Column(db.String, nullable=False)	
	is_public = db.Column(db.Boolean, default=False)

	@property
	def entry_list(self):
		return list(
			filter(None, self.entries.split(','))
		)
	
	@property
	def accessible_to_current_user(self):
		return self.is_public or (self.owner_id == current_user.user_id)

class TripEntry(db.Model):
	id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
	name = db.Column(db.String, nullable=False)
	geo_location = db.Column(db.String, nullable=False)
	people = db.Column(db.String, nullable=False, default="") # comma-separated list of people's names
	description = db.Column(db.String, nullable=False)
	rating = db.Column(db.Integer, nullable=False)
	added_at = db.Column(db.DateTime, nullable=False)
	images = db.Column(db.String, nullable=False, default="") # comma-separated list of image IDs
	parent_journey = db.Column(db.String, nullable=False)
	owner_id = db.Column(db.String, nullable=False)	
	is_public = db.Column(db.Boolean, default=False)

	@property
	def image_list(self):
		return list(
			filter(None, self.images.split(','))
		)

	@property
	def people_list(self):
		return list(
			filter(None, self.people.split(','))
		)

	@property
	def accessible_to_current_user(self):
		return self.is_public or (self.owner_id == current_user.user_id)

class Image(db.Model):
	id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
	data = db.Column(db.LargeBinary, nullable=False)
	owner_id = db.Column(db.String, nullable=False)
	is_public = db.Column(db.Boolean, default=False)

	@property
	def accessible_to_current_user(self):
		return self.is_public or (self.owner_id == current_user.user_id)
		
	def to_base64(self):
		return base64.b64encode(self.data).decode("ascii")


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
			"journeys": user.journey_list
		}
	)

@app.route("/api/createaccount")
@auth.require_user
def createaccount():
	try: user = User(id=current_user.user_id, username=request.args["username"])
	except KeyError: return Response(status=400) # 400 bad request

	db.session.add(user)
	db.session.commit()

	return Response(status=200) # 200 ok

@app.route("/api/listjourneys")
@auth.require_user
def listjourneys():
	user = db.session.execute(
		db.select(User).where(User.id == current_user.user_id)
	).scalar()

	if not user: return jsonify(None)

	return jsonify(user.journey_list)

@app.route("/api/getjourney")
@auth.require_user
def getjourney():
	journey: Journey = db.session.execute(
		db.select(Journey).where(Journey.id == request.args.get("id", ''))
	).scalar()

	if (
		(not journey) or # we must use an or and two nots so that we do not raise AttributeError from using a null value
		(not journey.accessible_to_current_user)
	): return jsonify(None)

	return jsonify({
		"id": journey.id, # echo
		"name": journey.name,
		"entries": journey.entry_list,
	})

@app.route("/api/getentry")
@auth.require_user
def getentry():
	entry: TripEntry = db.session.execute(
		db.select(TripEntry).where(TripEntry.id == request.args.get("id", ''))
	).scalar()

	if (
		(not entry) or # we must use an or and two nots so that we do not raise AttributeError from using a null value
		(not entry.accessible_to_current_user)
	): return jsonify(None)

	return jsonify({
		"id": entry.id, # echo
		"name": entry.name,
		"location": entry.geo_location,
		"description": entry.description,
		"images": entry.image_list,
		"people": entry.people_list,
		"rating": entry.rating,
		"timestamp": entry.added_at.isoformat()
	})

@app.route("/api/getphoto")
@auth.require_user
def getphoto():
	photo: Image = db.session.execute(
		db.select(Image).where(Image.id == request.args.get("id", ''))
	).scalar()

	if not photo: return jsonify(None)

	if (
		(not photo) or # we must use an or and two nots so that we do not raise AttributeError from using a null value
		(not photo.accessible_to_current_user)
	): return jsonify(None)

	return jsonify(photo.to_base64())

@app.route("/api/addentry")
@auth.require_user
def addentry():
	try:
		entry = TripEntry(
			id=genid.genid(),
			name=request.form["name"],
			geo_location=request.form["loc"],
			people=request.form["people"],
			description=request.form["description"],
			rating=int(request.form["rating"]),
			added_at=datetime.datetime.now(),
			parent_journey=request.form["journey"],
			owner_id=current_user.user_id
		)
	except (KeyError, ValueError): return Response(status=400) # 400 bad req

	db.session.add(entry)

	for file in request.files.values():
		img = Image(
			id=genid.genid(),
			data=file.stream.read(),
			owner_id=current_user.user_id
		)

		entry.images+=f"{img.id},"

		db.session.add(img)

	journey: Journey = db.session.execute(
		db.select(Journey).where(Journey.id == request.form["journey"])
	).scalar()

	if (
		(not journey) or # we must use an or and two nots so that we do not raise AttributeError from using a null value
		(not journey.accessible_to_current_user)
	): return Response(status=400) # 400 bad req

	journey.entries+=f"{entry.id},"

	db.session.commit()

	return Response(status=200) # 200 ok

@app.route("/api/createjourney")
@auth.require_user
def createjourney():
	name = request.args.get("name")

	if not name: return jsonify(None)

	journey = Journey(
		id=genid.genid(),
		name=name,
		owner_id=current_user.user_id
	)

	db.session.add(journey)
	db.session.commit()

	return jsonify(journey.id)


@app.route("/api/nearby")
@auth.require_user
def get_nearby_places():
	coord_string = request.args.get("loc")

	if not coord_string: return jsonify(None)

	try:
		split_string = coord_string.split(',')
		location: tuple[int, int] = int(split_string[0]), int(split_string[1])
	except (IndexError, ValueError):
		return jsonify(None)
	
	SEARCH_RADIUS_METERS = 100

	resp = maps.places_nearby(
		location=location,
		radius=SEARCH_RADIUS_METERS 
	)

	if resp["status"] != 200: return jsonify(None)

	results: dict = resp["results"]
	
	return jsonify(
		{
			place["name"]:
				f"{place['geometry']['location']['lat']},{place['geometry']['location']['lng']}"
			
			for place in results
		}
	)