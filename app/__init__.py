#app/__init__.py
#!flask/bin/python

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