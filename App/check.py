# from urllib.request import urlopen
# import requests
# import time
# from datetime import datetime
# import json
# url = "https://api.openweathermap.org/data/2.5/onecall?lat=33.44&lon=-94.04&exclude=hourly&appid=84ab8aee3c08e48f02450cc7580714cc"
# response  = urlopen(url)
#
# data_json = json.loads(response.read())
# # Step 3.
# pretty_json = json.dumps(data_json, indent=4)
# print(pretty_json)
# print(len(data_json['daily']))

#


# t =datetime.utcfromtimestamp(1641924474).strftime('%D %r')
# print(t)
# date_time_obj = datetime.strptime(t[3], '%h:%m:%s')
# # print(date_time_obj)

# from geocoding import direct_geocoding
#
# print(direct_geocoding('pune'))


# from geopy.geocoders import Nominatim
#
# # calling the Nominatim tool
# loc = Nominatim(user_agent="geoloc")
#
# # entering the location name
# get_loc = loc.geocode('Sydney')
#
# # printing address
# print(get_loc.address.split(",")[0])
# # print(getLoc.city)
# # printing latitude and longitude
# print("Latitude = ", getLoc.latitude, "\n")
# print("Longitude = ", getLoc.longitude)
# abc = loc.reverse(str(getLoc.latitude)+" "+str(getLoc.longitude))
# print(abc)
#
# address = getLoc.raw['address']
# print(address)

# print({"12.3:.2f"},1.233)


# num = 1.23232
#
# print(int(num))


from flask import Flask
from App.weather import weather

app = Flask(__name__)
app.config.from_pyfile('config/config.cfg')
w = weather(app.config)
while True:
    print("Enter the location")
    location = input()
    w.set_location(location)
    print(w.get_location())
    print(w.daily_weather_data)
    print(w.day)
    print(w.week)
    print(w.rain_data)
    print(w.rain_desc)
    print(w.temp_desc)
    print(w.wind_desc)
    print(w.humidity_desc)
    print(w.pressure_desc)
    print(w.cloud_desc)
    print(w.weather_desc)
    print(w.weather_icon)