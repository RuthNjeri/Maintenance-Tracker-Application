#app/__init__.py
#!flask/bin/python


from flask import Flask
from config.config import app_config




#Initialize application
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    # app.config.from_pyfile('app.config')

    return app

   

app = create_app('development')