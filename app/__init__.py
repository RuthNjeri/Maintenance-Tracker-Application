#app/__init__.py

from flask import Flask


#Initialize application
app = Flask(__name__,instance_relative_config=True)



#Load config file
app.config.from_object('config')