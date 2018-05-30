#app/__init__.py

from flask_api import FlaskAPI
from instance.config import app_config


#Initialize application
def create_app(config_name):
    app = FlaskAPI(__name__,instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    return app



