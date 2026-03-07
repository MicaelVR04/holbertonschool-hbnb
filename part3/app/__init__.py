from flask import Flask
from app.api import blueprint


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register API blueprint
    app.register_blueprint(blueprint)

    return app
