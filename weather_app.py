from flask import Flask, render_template, request, redirect, url_for
from geopy.geocoders import Nominatim
from weather import weather

app = Flask(__name__)
app.config.from_pyfile('config/config.cfg')
#
# w = weather(app.config)
w = weather(app.config)


# while True:
#     print("Enter the location")
#     location = input()
#     w.set_location(location)
#     print(w.get_location())
#     print(w.daily_weather_data)
#     print(w.get_day())
#     print(w.get_week())
#     print(w.get_predicted_data())


@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        location = request.form
        w.set_location(location.get('location'))
    else:
        w.set_location('pune')
        redirect("/")
    return render_template('index.html', location=w.get_location(), day=w.day, week=w.week, data=w.daily_weather_data,
                           pdata=w.rain_data, rain_desc=w.rain_desc, temp_desc=w.temp_desc, wind_desc=w.wind_desc,
                           humidity_desc=w.humidity_desc, pressure_desc=w.pressure_desc, clouds_desc=w.cloud_desc,
                           weather_icon=w.weather_icon, weather_desc=w.weather_desc)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return  render_template('register.html')


@app.route('/profile')
@app.route('/location')
@app.route('/about')
def soon():
    return "<h1> Updating soon </h1>"


#
#
# @app.route('/result', methods=['GET', 'POST'])
# def location_result():
#     loc = Nominatim(user_agent="geoloc")
#     getLoc = None
#     if request.method == 'POST':
#         location = request.form
#         print(location.get('location'))
#         getLoc = loc.geocode(location.get('location'))
#         print(getLoc.address)
#     return render_template(['index.html', 'searchbar.html'],
#                            location=getLoc.address.split(",")[0] + " " + getLoc.address.split(",")[-1])
#


if __name__ == '__main__':
    app.run(debug=True)
