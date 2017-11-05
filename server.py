from flask import Flask, request, redirect, render_template
import requests
import ssl
import json 

print(ssl.OPENSSL_VERSION)

app = Flask(__name__)
API_KEY = '7c791a9b70cc0570c13fdb3cff7cede3'


@app.route("/")
def index():
	return render_template('index.html')	

@app.route('/weather',methods=['GET','POST'])
def get_weather():
	zipc = request.form['zipc']
	new_url = '/weather/'+zipc
	return redirect(new_url)

@app.route('/weather/<zipc>')
def get_weather_for_zip(zipc):
	url = 'https://api.openweathermap.org/data/2.5/weather?zip='+zipc+',us&APPID='+API_KEY
	r = requests.get(url,verify=False)
	info = r.json()
	town = info['name'].upper()
	deg = str((int(info['main']['temp'])*9/5) - 459.67).split('.')[0]
	desc = 'Today in '  + info['name'] + ', it is ' + deg + ' degrees. You may experience '
	weathers = []
	for w in info['weather']:
		weathers.append(w['description'])
		desc += (w['description'] + ', ')
	sw = True
	if (int(deg) > 62):
		sw = False
	return render_template('weather.html', sw=sw, town=town, weathers=weathers, deg=deg, info=desc)		

if __name__ == "__main__":
    app.run(debug=True)