# project/app.py

# imports
import os
from flask import Flask
# blueprints
from project.requests.views import trackerapp
from project.users.views import users

# configuration
app = Flask(__name__)

# register blueprints
app.register_blueprint(users, url_prefix='/api/v2')
app.register_blueprint(trackerapp, url_prefix='/api/v2')

# app configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'project.config.DevConfig'
)
app.config.from_object(app_settings)
