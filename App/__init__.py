from flask import Flask
from flask_sqlalchemy import  SQLAlchemy
from flask_redis import FlaskRedis

db = SQLAlchemy()
r = FlaskRedis()


def init_app():
    app = Flask(__name__,instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)
    r.init_app(app)

    with app.app_context():
        from . import routes

        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(admin.admin_bp)

        return app