#project/app.py

#imports
import os
from flask import Flask
from . import config
#blueprints
from project.requests.views import requests
from project.users.views import users




#configuration
app = Flask(__name__)

#register blueprints
app.register_blueprint(users, url_prefix='/api/v2')
app.register_blueprint(requests, url_prefix='/api/v2')

# app configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'project.config.DevConfig'
)
app.config.from_object(app_settings)





