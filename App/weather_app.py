from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from App.weather import weather

app = Flask(__name__)
app.config.from_pyfile('config/config.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# noinspection PyUnresolvedReferences
class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

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


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        mail = request.form['mail']
        passw = request.form['passw']
        login = user.query.filter_by(email = mail,password=passw).first()
        if login is not None:
            return redirect('/')
    return render_template('login.html')


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']
        register = user(username = uname,email = mail, password = passw)
        db.session.add(register)
        db.session.commit()
        return redirect(url_for("login"))
    return  render_template('signup.html')

@app.route('/location')
def location():
    return render_template('location.html')
@app.route('/profile')
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
    app.run()
