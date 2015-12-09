from flask import Flask

from .views import site

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(site)

    return app
