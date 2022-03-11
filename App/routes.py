from flask_login import current_user, login_user, login_required, logout_user
from flask import Blueprint, flash, redirect, url_for, render_template, request
from App.forms import LoginForm, RegForm
from App.models import User, location
from App import app, db, pwd, w

main_bp = Blueprint(
    'main_bp', __name__,
    static_folder='static',
    template_folder='templates'
)


@main_bp.route('/', methods=['GET', 'POST'])
@login_required
def homepage():
    if request.method == 'POST':
        loc = request.form
        w.set_location(loc.get('location'))
    else:
        w.set_location('pune')
        redirect("/")
    return render_template('index.html', location=w.get_location(), day=w.day, week=w.week, data=w.daily_weather_data,
                           pdata=w.rain_data, rain_desc=w.rain_desc, temp_desc=w.temp_desc, wind_desc=w.wind_desc,
                           humidity_desc=w.humidity_desc, pressure_desc=w.pressure_desc, clouds_desc=w.cloud_desc,
                           weather_icon=w.weather_icon, weather_desc=w.weather_desc)


@main_bp.route('/location', methods=['GET', 'POST'])
@login_required
def add_location():
    loc = location.query.filter_by(user_id = 1).all()

    if request.method == 'POST':
        loc = request.form
        w.set_location(loc.get('location'))
    else:
        w.set_location('pune')
        redirect("/")
    return render_template('location.html', location=loc, day=w.day, week=w.week,
                           data=w.daily_weather_data,
                           pdata=w.rain_data, rain_desc=w.rain_desc, temp_desc=w.temp_desc, wind_desc=w.wind_desc,
                           humidity_desc=w.humidity_desc, pressure_desc=w.pressure_desc, clouds_desc=w.cloud_desc,
                           weather_icon=w.weather_icon, weather_desc=w.weather_desc)


@main_bp.route("/logout")
def logoutpage():
    logout_user()
    flash("Your successfully logout")
    return redirect(url_for("main_bp.loginpage"))


@main_bp.route('/about')
def soon():
    return "<h1> Updating soon </h1>"


@main_bp.route('/signup', methods=['GET', 'POST'])
def signuppage():
    if current_user.is_authenticated:
        flash("You are already logged in.", "warning")
        return redirect(url_for("homepage"))
    form = RegForm(request.form)
    if request.method == "POST" and form.validate():
        hashed = pwd.generate_password_hash(form.password.data).decode('utf-8')
        element = User(uname=form.uname.data, email=form.email.data, password=hashed)
        db.session.add(element)
        db.session.commit()
        flash("Account created for %s!" % form.uname.data, "success")
        return redirect(url_for("main_bp.loginpage"))
    return render_template("signup.html", form=form)


@main_bp.route('/login', methods=['GET', 'POST'])
def loginpage():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.homepage"))
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        member = User.query.filter_by(email=form.email.data).first()
        if member and pwd.check_password_hash(member.password, form.password.data):
            login_user(member)
            return redirect(url_for("main_bp.homepage"))
        else:
            flash("Email or Password doesn't match, please try again.", "is-danger")
            return redirect(url_for("main_bp.loginpage"))
    return render_template("login.html", form=form)


# @main_bp.route('/location', methods=['GET', 'POST'])
# def location():
#     pass


if __name__ == '__main__':
    app.run()
