from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.models.base_model import db

bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config["JWT_SECRET_KEY"] = app.config["SECRET_KEY"]

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from app.api import blueprint
    app.register_blueprint(blueprint)

    return app
