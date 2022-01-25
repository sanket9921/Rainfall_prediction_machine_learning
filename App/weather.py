import requests
import joblib
from geopy.geocoders import Nominatim
from datetime import datetime

API_KEY = '84ab8aee3c08e48f02450cc7580714cc'
API_URL = 'https://api.openweathermap.org/data/2.5/onecall'


class WeatherException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None


class weather:
    def __init__(self):
        self.__model = None
        self.location = None
        self.__loc = None
        self.latitude = None
        self.longitude = None
        self.address = None

        self.week = []
        self.day = []
        self.date = []
        self.weather_data = None
        self.daily_weather_data = []
        self.rain_data = []
        self.rain_desc = []
        self.temp_desc = []
        self.wind_desc = []
        self.humidity_desc = []
        self.pressure_desc = []
        self.cloud_desc = []
        self.__load_model()
        self.weather_desc = []
        self.weather_icon = []

    def __load_model(self):
        self.__model = joblib.load(open('App/RF-model/Rainfall_best_model13.pkl', 'rb'))
        self.__loc = Nominatim(user_agent="GetLoc")

    def __initialise(self):
        self.week = []
        self.day = []
        self.date = []
        self.weather_data = None
        self.daily_weather_data = []
        self.rain_data = []
        self.rain_desc = []
        self.temp_desc = []
        self.wind_desc = []
        self.humidity_desc = []
        self.pressure_desc = []
        self.cloud_desc = []
        self.weather_desc = []
        self.weather_icon = []
        self.step_collect_data()

    def set_location(self, location):
        self.location = location
        get_loc = self.__loc.geocode(self.location)
        self.latitude = get_loc.latitude
        self.longitude = get_loc.longitude
        self.address = get_loc.address
        self.__initialise()

    def step_collect_data(self):
        self.__download_weather_data()
        self.__set_daily_weather_data()
        self.__set_day_week()
        self.get_predicted_data()
        self.rain_description()
        self.other_description()

    def get_location(self):
        return self.address.split(',')[0] + self.address.split(',')[-1]

    def get_day(self):
        return self.day

    def get_week(self):
        return self.week

    def get_predicted_data(self):
        predicted = self.__model.predict(self.daily_weather_data)
        self.rain_data = [int(a) for a in predicted]
        # return self.predict_data

    def get_daily_weather_data(self):
        return self.daily_weather_data

    def __download_weather_data(self):
        try:

            params = {
                'lat': self.latitude,
                'lon': self.longitude,
                'units': 'metric',
                'appid': API_KEY
            }

            response = requests.get(API_URL, params=params)
            response.raise_for_status()
            self.weather_data = response.json()
        except requests.exceptions.HTTPError:

            raise WeatherException("Weather for {} not found".format(self.location))

    def __set_day_week(self):
        for i in self.date:
            date = datetime.utcfromtimestamp(i)
            self.day.append(date.strftime("%d/%m/%y"))
            self.week.append(date.strftime("%A"))

    def __set_daily_weather_data(self):
        for i in range(0, len(self.weather_data['daily'])):
            self.date.append(self.weather_data['daily'][i]['dt'])
            MinTemp = self.weather_data['daily'][i]['temp']['min']
            MaxTemp = self.weather_data['daily'][i]['temp']['max']
            WindGustSpeed = self.weather_data['daily'][i]['wind_gust']
            WindDir = self.weather_data['daily'][i]['wind_deg']
            WindSpeed = self.weather_data['daily'][i]['wind_speed']
            Humidity = self.weather_data['daily'][i]['humidity']
            Pressure = self.weather_data['daily'][i]['pressure']
            Cloud = self.weather_data['daily'][i]['clouds']
            Temp9am = self.weather_data['daily'][i]['temp']['morn']
            Temp3pm = self.weather_data['daily'][i]['temp']['eve']

            self.weather_desc.append(self.weather_data['daily'][i]['weather'][0]['description'])
            self.weather_icon.append(self.weather_data['daily'][i]['weather'][0]['icon'])

            self.daily_weather_data.append(
                [MinTemp, MaxTemp, WindGustSpeed, WindDir, WindSpeed, Humidity, Pressure, Cloud, Temp9am, Temp3pm])

    def __set_hourly_weather_data(self):
        pass

    def rain_description(self):
        for i in self.rain_data:
            if i >= 8:
                self.rain_desc.append("Very Heavy Rain")
            elif i >= 4:
                self.rain_desc.append("Heavy Rain")
            elif i >= 2:
                self.rain_desc.append("Moderate Rain")
            elif i >= 1:
                self.rain_desc.append("Light Rain")
            else:
                self.rain_desc.append("NO Rain")

    def other_description(self):
        for i in self.daily_weather_data:

            # temperature description
            if i[1] > 30:
                self.temp_desc.append("high")
            elif i[1] > 20:
                self.temp_desc.append("medium")
            else:
                self.temp_desc.append("low")

            # wind speed description
            if i[4] > 30:
                self.wind_desc.append("high")
            elif i[4] > 20:
                self.wind_desc.append("medium")
            else:
                self.wind_desc.append("low")

            # humidity description
            if i[5] > 50:
                self.humidity_desc.append("high")
            elif i[5] > 30:
                self.humidity_desc.append("medium")
            else:
                self.humidity_desc.append("low")

            # pressure description
            if i[6] > 1022:
                self.pressure_desc.append("high")
            elif i[6] > 1009:
                self.pressure_desc.append("medium")
            else:
                self.pressure_desc.append("low")

            # cloud cover desc
            if i[7] > 60:
                self.cloud_desc.append("high")
            elif i[7] > 30:
                self.cloud_desc.append("medium")
            else:
                self.cloud_desc.append("low")
