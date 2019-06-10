########################################################
# dependencies:
# 	flask
# 	tensorflow
# 	requests
# 	numpy

# for windows cmd terminal
# set FLASK_APP=flaskr
# set FLASK_ENV=development

# for mac/linux terminal
# export FLASK_APP=flaskr
# export FLASK_ENV=development

# flask run --without-threads
########################################################

import os

from flask import Flask

def create_app(test_config=None):
	#create and configure the app
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
	)

	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)
	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass
	#create_app(test_config=None)
	# a simple page that says hello
	@app.route('/hello')
	def hello():
		return 'Hello!'

	from . import db
	db.init_app(app)

	from . import auth
	app.register_blueprint(auth.bp)

	from . import weather
	app.register_blueprint(weather.bp)
	app.add_url_rule('/', endpoint='index')
	
	return app