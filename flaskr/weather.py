from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

import requests
import numpy as np
from flask import jsonify, current_app
import pickle
import json
import numpy as np
import googlemaps
import time

# Load the model
#model = pickle.load(open('modell.pkl','rb'))


bp = Blueprint('weather',__name__)

@bp.route('/',methods=('GET','POST'))
@login_required
def index():
	#return render_template('auth/login.html')
	return render_template('weather/index.html')

@bp.route('/home',methods=('GET','POST'))
@login_required
def home():
	#print(session.get('model'))
	#print('home')
	return render_template('weather/home.html')
	#return render_template('weather/index.html')



@bp.route('/predict', methods=('GET','POST'))
@login_required
def predict():
	if request.method=='POST':
		#gmaps = googlemaps.Client(key='AIzaSyCKDz2le7flatBRk2tlKSPHQkWOb-JnIaM')
		weather_api_openweathermap = 'f556fafd24efcd2934d9ed1a86b8374d'
		default_country = 'in'
		city_name = request.form['city_name']

		weather_api_darksky = '39cfb4d6c9cd0113694846cc3f388a2c' # create account at https://darksky.net/dev/
		weather_lang = 'en'
		weather_unit = 'si'

		scale_factor = 4733.25

		# geo_details = gmaps.geocode(city_name+','+default_country)
		# lat = geo_details[0]['geometry']['location']['lat']
		# lng = geo_details[0]['geometry']['location']['lng']
		#print(city_name)

		# Hour ; Day ; Month ; Year ; Cloud Coverage ; Visibility ; Temperature ; Dew Point ;
		# Relative Humidity ; Wind Speed ; Station Pressure ; Altimeter


		#'https://api.openweathermap.org/data/2.5/weather?q=pune,in&appid=f556fafd24efcd2934d9ed1a86b8374d'
		url_openweathermap = 'https://api.openweathermap.org/data/2.5/weather?q={},{}&appid={}'.format(city_name, default_country, weather_api_openweathermap)
		try:
			openweathermap_data = requests.get(url_openweathermap).json()
		except:
			abort(502, 'Check connection.')
			#return render_template('weather/error.html')

		#print(url_openweathermap)

		#  sample api response		
		# {'coord': {'lon': 73.85, 'lat': 18.52}, 
		#  'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}],
		#  'base': 'stations', 
		#  'main': {'temp': 305.205, 'pressure': 1008.86, 'humidity': 27, 'temp_min': 305.205, 'temp_max': 305.205, 'sea_level': 1008.86, 'grnd_level': 927.09}, 
		#  'wind': {'speed': 4.88, 'deg': 288.442}, 
		#  'clouds': {'all': 0}, 
		#  'dt': 1557925845, 
		#  'sys': {'message': 0.0044, 'country': 'IN', 'sunrise': 1557880271, 'sunset': 1557927052}, 
		#  'id': 1259229, 'name': 'Pune', 'cod': 200}

		lat = openweathermap_data['coord']['lat']
		lng = openweathermap_data['coord']['lon']	
		#time.struct_time(tm_year=2019, tm_mon=5, tm_mday=15, tm_hour=19, tm_min=0, tm_sec=57, tm_wday=2, tm_yday=135, tm_isdst=0)	
		date_time = time.localtime(openweathermap_data['dt'])
		hour = date_time[3]
		day = date_time[2]
		month = date_time[1]
		year = date_time[0]
		temperature = openweathermap_data['main']['temp'] - 273.15
		relative_humidity = openweathermap_data['main']['humidity']
		wind_speed = openweathermap_data['wind']['speed']
		station_pressure = openweathermap_data['main']['pressure']
		altimeter = openweathermap_data['main']['pressure']

		#'https://api.darksky.net/forecast/39cfb4d6c9cd0113694846cc3f388a2c/18.5204303,73.8567437'
		url_darksky = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_darksky, lat, lng, weather_lang, weather_unit)
		try:
			darksky_data = requests.get(url_darksky).json().get('currently')
		except:
			abort(502, 'Check connection.')
			#return render_template('weather/error.html')

		# {'time': 1557925526, 'summary': 'Clear', 'icon': 'clear-day', 'precipIntensity': 0, 'precipProbability': 0, 
		# 'temperature': 92.51, 'apparentTemperature': 92.51, 'dewPoint': 47.96, 'humidity': 0.22, 'pressure': 1008.31, 
		# 'windSpeed': 12.2, 'windGust': 15.75, 'windBearing': 286, 'cloudCover': 0, 'uvIndex': 0, 'visibility': 10, 'ozone': 278.13}

		visibility = darksky_data['visibility']
		cloud_coverage = darksky_data['cloudCover']
		dew_point = darksky_data['dewPoint']


	


		'''
		model = None

		with current_app.open_resource('modell.pkl','rb') as f:
			model = pickle.load(f.read())
		'''

		#model = pickle.load(open(url_for('static', filename='modell.pkl'),'rb'))
		#model = session.get('model')
		model = pickle.load(open('/Users/aniket/SolarPowerPredictor/flaskr/static/modell.pkl','rb'))
		# model = pickle.load(open('static/modell.pkl','rb'))
		# path = url_for('static', filename='modell.pkl')
		# print(path)
		#model = pickle.load(open(path, 'rb'))

		params = {"hour":hour, "day":day, "month":month, "year":year, "cloud_coverage":cloud_coverage, "visibility":visibility, 
			"temperature":temperature, "dew_point":dew_point, "relative_humidity":relative_humidity, 
			"wind_speed":wind_speed, "station_pressure":station_pressure, "altimeter":altimeter}
		
		#data1 = [0.545455,0.0333333,0,1,1,0.185,0.489233,0.576471,0.979147,0.262753,0.963205,0.908989]
		data1 = np.array([hour, day, month, year, cloud_coverage, visibility, temperature, 
			dew_point, relative_humidity, wind_speed, station_pressure, altimeter]).astype('float32')/scale_factor
		#data1 = process_data([])

		exp=np.reshape(data1,(1,1,12))
		print(exp)
		print("++++++++++++++++++++")
		# Make prediction using model loaded from disk as per the data.
		#response={}
		response= model.predict(exp)[0][0][0]
		response *= scale_factor
		print(response)
		session['predict_result']=response
		session['params']=params
		#return str(response)
		return render_template('weather/predict.html')
		#return render_template('weather/predict.html')
		#return jsonify(response)



		#return render_template('weather/predict.html')
	#return render_template('weather/predict.html')
	return redirect(url_for('index'))
