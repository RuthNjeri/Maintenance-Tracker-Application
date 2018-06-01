#app/__init__.py
#!flask/bin/python

<<<<<<< HEAD
import os
from flask import Flask
from . import config
# from config.config import app_config




# #Initialize application
# def create_app(config_name):
#     app = Flask(__name__)
#     app.config.from_object(app_config[config_name])


#     return app

   

# app = create_app('development')


app = Flask(__name__, static_folder=None)

# app configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevConfig'
)
app.config.from_object(app_settings)


# Import the application views
from app import views
=======

from flask import Flask
from config.config import app_config




#Initialize application
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    # app.config.from_pyfile('app.config')

    return app

   

app = create_app('development')
>>>>>>> 2ddb97ca05298ac7af2558e95407c1ec86a0dfb5
