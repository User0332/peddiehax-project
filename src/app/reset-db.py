import app

with app.app.app_context():
	app.db.create_all()