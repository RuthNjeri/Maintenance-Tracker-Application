#app/__init__.py
#!flask/bin/python

import os
from flask import Flask
from . import config





app = Flask(__name__)

# app configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevConfig'
)
app.config.from_object(app_settings)


# Import the application views
from app import views