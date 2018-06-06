#project/app.py

#imports
import os
from flask import Flask
from . import config
#blueprints
from .requests.views import requests
from .users.views import users




#configuration
app = Flask(__name__)

#register blueprints
app.register_blueprint(users)
app.register_blueprint(requests)

# app configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'project.config.DevConfig'
)
app.config.from_object(app_settings)





