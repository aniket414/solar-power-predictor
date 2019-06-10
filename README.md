# SolarPowerPredictor

Dependencies:
	Python
	flask
	pickle
	tensorflow
	requests
	numpy

In the 
	
	"SolarPowerPredictor/flaskr/weather.py" 

Goto Line 127 and specify the path where modell.pkl is stored. As in my case it is 
	
	"/Users/aniket/SolarPowerPredictor/flaskr/static/modell.pkl"

To start the Server, Goto SolarPowerPredictor folder in terminal and follow the steps mentioned.

For windows cmd terminal

	set FLASK_APP=flaskr
	set FLASK_ENV=development
	flask run --without-threads

For mac/linux terminal

	export FLASK_APP=flaskr
	export FLASK_ENV=development
	flask run --without-threads

Now open Web Browser and Goto
	
	127.0.0.1:5000

