from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from App.weather import weather

w = weather()

app = Flask(__name__, instance_relative_config=False)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
pwd = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'main_bp.loginpage'
login_manager.login_message = 'You are not authorised to access page. Please login first'
login_manager.login_message = 'Please Login first'

with app.app_context():
    from . import routes
    app.register_blueprint(routes.main_bp)
