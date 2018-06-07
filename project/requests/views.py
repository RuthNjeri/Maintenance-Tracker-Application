# project/requests/views.py

# imports
import datetime
import jwt
import psycopg2
from flask import Flask, request, jsonify, abort, make_response, Blueprint
from project.config import conn, Config
from project.users.views import decode_auth_token



# configure blueprint
trackerapp = Blueprint('trackerapp', __name__, template_folder='templates')
#create cursor to connect to the database
cur = conn.cursor()


def get_token():
    #get the JWT token
    token = request.headers.get('token', None)
    return token


@trackerapp.route('/tracker')
def index():
    return "hello tracker"

@trackerapp.errorhandler(404)
def request_not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@trackerapp.route('/users/requests',methods=['POST'])
def user_create_request():
    token = get_token()
    if token:
        form = request.get_json()
        title = form['title']
        description= form['description']
        status = form['status']
        




