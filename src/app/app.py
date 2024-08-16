from webpy import App
import sys
import os

sys.path.append(
	os.path.join(
		os.getcwd(),
		"glblib"
	)
)

app = App(__name__, template_folder="html")

def webpy_setup(app: App):
	app.debug = True