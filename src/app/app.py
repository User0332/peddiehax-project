import datetime
import random
import secrets
import base64
import time
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
	ftype = db.Column(db.String, nullable=False)

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
		"owner": journey.owner_id
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
		"timestamp": entry.added_at.isoformat(),
		"journey": entry.parent_journey
	})

@app.route("/api/getphoto")
@auth.require_user
def getphoto():
	photo: Image | None = db.session.execute(
		db.select(Image).where(Image.id == request.args.get("id", ''))
	).scalar()

	if not photo: return jsonify(None)

	if (
		(not photo) or # we must use an or and two nots so that we do not raise AttributeError from using a null value
		(not photo.accessible_to_current_user)
	): return jsonify(None)

	return jsonify(f"data:image/{photo.ftype};base64,{photo.to_base64()}")

@app.route("/api/addentry", methods=["POST"])
@auth.require_user
def addentry():
	journey: Journey = db.session.execute(
		db.select(Journey).where(Journey.id == request.form.get("journey", ''))
	).scalar()

	if (
		(not journey) or # we must use an or and two nots so that we do not raise AttributeError from using a null value
		(not journey.owner_id == current_user.user_id)
	): return Response(status=400) # 400 bad req

	try:
		entry = TripEntry(
			id=genid.genid(),
			name=request.form["name"],
			geo_location=request.form["loc"],
			people=request.form["people"],
			description=request.form["description"],
			rating=int(request.form["rating"]),
			added_at=datetime.datetime.now(),
			parent_journey=journey.id,
			owner_id=current_user.user_id,
			images=""
		)
	except (KeyError, ValueError): return Response(status=400) # 400 bad req

	entry.is_public = journey.is_public

	db.session.add(entry)

	for file in request.files.values():
		img = Image(
			id=genid.genid(),
			data=file.stream.read(),
			owner_id=current_user.user_id,
			ftype=file.filename.split('.')[-1],
			is_public=entry.is_public
		)

		entry.images+=f"{img.id},"

		db.session.add(img)


	journey.entries+=f"{entry.id},"

	db.session.commit()

	return Response(status=200) # 200 ok

@app.route("/api/createjourney")
@auth.require_user
def createjourney():
	name = request.args.get("name")
	is_public = request.args.get("public").lower() == "true"

	if not name: return jsonify(None)

	journey = Journey(
		id=genid.genid(),
		name=name,
		owner_id=current_user.user_id,
		is_public=is_public
	)

	db.session.add(journey)

	user: User | None = db.session.execute(
		db.select(User).where(User.id == current_user.user_id)
	).scalar()

	if not user: return jsonify(None)

	user.journeys+=f"{journey.id},"

	db.session.commit()

	return jsonify(journey.id)


@app.route("/api/nearby")
@auth.require_user
def get_nearby_places():
	coord_string = request.args.get("loc")

	if not coord_string: return jsonify(None)

	try:
		split_string = coord_string.split(',')
		location: tuple[float, float] = float(split_string[0]), float(split_string[1])
	except (IndexError, ValueError):
		return jsonify(None)
		
	SEARCH_RADIUS_METERS = 50

	results: list[dict] = []

	resp = maps.places_nearby(
		location=location,
		radius=SEARCH_RADIUS_METERS 
	)

	if resp["status"] != "OK": return jsonify(None)

	results.extend(resp["results"])

	while "next_page_token" in resp:
		time.sleep(0.7) # reduce number of API requests
		try: resp = maps.places_nearby(page_token=resp["next_page_token"])
		except googlemaps.exceptions.ApiError: continue # it takes a little while to activate the next page token, so keep requesting until we can

		results.extend(resp["results"])
	
	return jsonify(
		{
			place["name"]:
				f"{place['geometry']['location']['lat']},{place['geometry']['location']['lng']}"
			
			for place in results
		}
	)

def delentry_noroute(entry_id: str):
	entry: TripEntry | None = db.session.execute(
		db.select(TripEntry).where(TripEntry.id == entry_id)
	).scalar()

	if (
		(not entry) or
		(not entry.accessible_to_current_user)
	): return False

	for image_id in entry.image_list:
		img: Image | None = db.session.execute(
			db.select(Image).where(Image.id == image_id)
		).scalar()

		db.session.delete(img)

	db.session.delete(entry)
	db.session.commit()

	return True

def deljourney_noroute(journey_id: str):
	journey: Journey | None = db.session.execute(
		db.select(Journey).where(Journey.id == journey_id)
	).scalar()

	if (
		(not journey) or
		(not journey.accessible_to_current_user)
	): return False

	for entry_id in journey.entry_list:
		delentry_noroute(entry_id)

	db.session.delete(journey)
	db.session.commit()

	return True

@app.route("/api/deljourney")
@auth.require_user
def deljourney():
	if not deljourney_noroute(request.args.get("id")): return Response(status=400)

	return Response(status=200)


@app.route("/api/delentry")
@auth.require_user
def delentry():
	if not delentry_noroute(request.args.get("id")): return Response(status=400)

	return Response(status=200)

@app.route("/api/deluser")
@auth.require_user
def deluser():
	user: User | None = db.session.execute(
		db.select(User).where(User.id == current_user.user_id)
	).scalar()

	if user:
		for journey_id in user.journey_list:
			deljourney_noroute(journey_id)

		db.session.delete(user)
		db.session.commit()

	auth.delete_user(current_user.user_id)

	return Response(status=200) # 200 ok

@app.route("/api/getplotdata")
@auth.require_user
def getplotdata():
	journey: Journey = db.session.execute(
		db.select(Journey).where(Journey.id == request.args.get("id", ''))
	).scalar()

	if (
		(not journey) or
		(not journey.accessible_to_current_user)
	): return jsonify(None)

	entries: list[str] =  journey.entry_list

	if len(entries) < 2: return jsonify(None) # not enough entries to plot

	path: list[str] = []

	for entry_id in entries:
		path.append(
			db.session.execute(
				db.select(TripEntry).where(TripEntry.id == entry_id)
			).scalar().name
		)

	while len(path) > 22:
		path.pop(random.randint(1, 20)) # remove random items in the middle

	return jsonify({
		"src": path[0],
		"waypoints": path[1:-1],
		"dst": path[-1]
	})

@app.route("/api/getfeed")
@auth.require_user
def getfeed(): # TODO: make post creation API accept is_public param, create frontend for viewing feed
	posts: list[Journey] = list(
		db.session.execute(
			db.select(Journey).where(Journey.is_public == True)
		).scalars().all()
	)

	if len(posts) <= 3: return jsonify([
		post.id for post in posts
	])

	return jsonify([
		post.id for post in random.sample(posts, 3)
	])

@app.route("/api/getuser")
@auth.require_user
def getuser():
	user = db.session.execute(
		db.select(User).where(User.id == request.args.get("id"))
	).scalar()

	if not user: return jsonify(None)

	return jsonify(
		{
			"username": user.username,
			"id": user.id,
			"journeys": user.journey_list
		}
	)