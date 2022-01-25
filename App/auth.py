from flask import Blueprint, flash, redirect, url_for, render_template, request
from flask_login import current_user, login_user
from App.forms import LoginForm, RegForm
from App.models import User
from App import pwd, db

auth_bp = Blueprint(
    'auth_bp', __name__,
    static_folder='static',
    template_folder='templates'
)


@auth_bp.route('/signup', methods=['GET', 'POST'])
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
        return redirect(url_for("auth_bp.loginpage"))
    return render_template("signup.html", form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def loginpage():
    if current_user.is_authenticated:
        flash("You are already logged in.", "warning")
        return redirect(url_for("main_bp.homepage"))
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        member = User.query.filter_by(email=form.email.data).first()
        if member and pwd.check_password_hash(member.password, form.password.data):
            login_user(member)
            flash("Welcome, %s!" % form.email.data, "success")
            return redirect(url_for("main_bp.homepage"))
        else:
            flash("Email or Password doesn't match, please try again.", "is-danger")
            return redirect(url_for("auth_bp.loginpage"))
    return render_template("login.html", form=form)
