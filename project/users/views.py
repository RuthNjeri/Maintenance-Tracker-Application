# project/users/views.py 

# imports
import datetime
import jwt
import psycopg2
from flask import Flask, request, jsonify, abort, make_response, Blueprint, render_template,redirect, url_for
from validate_email import validate_email
from werkzeug.security import check_password_hash
from project.config import Config
from project.database import User


"""
Create an object to perform database queries from the database class in project/database.py
"""
email = ""
first_name = ""
last_name = ""
password = ""
db = User(email, first_name, last_name, password)

"""
Configure blueprint
"""
users = Blueprint('users', __name__, template_folder='templates')


def jwt_auth_encode(userid):
    """
    Generate the user authentication token
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=3600),
            'iat': datetime.datetime.utcnow(),
            'sub': userid
        }
        return jwt.encode(
            payload,
            Config.SECRET
        )
    except Exception as e:
        raise e


def decode_auth_token(auth_token):
    """
    Decode the user authentication token
    """
    try:
        payload = jwt.decode(auth_token, Config.SECRET)
        return payload['sub']
    except Exception as e:
        return None

@users.app_errorhandler(404)
def request_not_found(error):
    """
    Response for requests to endpoints that do not exist
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


@users.route('/auth/signup', methods=['POST', 'GET'])
def create_user():


    try:
        """
        Endpoint to register a user with the details below
        """
        form = request.get_json()
        email = form['email']
        first_name = form['first_name']
        last_name = form['last_name']
        password = form['password']
        confirm_password = form['confirm_password']
        """
        Validate user input
        """
        valid_email = validate_email(email)
        if email == "":
            return jsonify({'response': 'email cannot be empty'}), 409
        if not valid_email:
            return jsonify({'response': 'enter email in correct format'}), 409
        if password == "":
            return jsonify({'response': 'password cannot be empty'}), 409
        if password != confirm_password:
            return jsonify({'response': 'password does not match'}), 409
        if len(password) < 8:
            return jsonify({'response': 'password must be 8 values or more'}), 409
        """
        search if the user exists in the database
        """
        register_user = User(email, first_name, last_name, password)
        register_user.user_email_exists()
        if register_user.user is None:
            register_user.create_user()
            return jsonify({'redirect_url': url_for('users.login_user'), 'successful': True}), 200
        else:
            return jsonify({'response': 'user already exists'}), 409

    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as e:
        print('error', e)
        return render_template('signUp.html')


@users.route('/auth/login', methods=['POST', 'GET'])
def login_user():

    try:
        """
        Endpoint to login user with details below
        """
        form = request.get_json()
        email = form['email']
        password = form['password']
        first_name = ""
        last_name = ""
        """
        look for the user in the database and compare passwords
        """
        login_user = User(email, first_name, last_name, password)
        login_user.user_email_exists()

        if login_user.user == None :
            """
            if the email does not exist
            """
            return jsonify({'response': 'Please enter the correct user details'}), 409

        if check_password_hash(login_user.user[4], password):
            """
            Provide token if user password is correct
            """
            token = jwt_auth_encode(login_user.user[0])
            if token:
                response = {'token': token.decode(),'successful': True
                            }
                return jsonify(response), 200
        else:
            return jsonify({'response': 'Please enter the correct user details'}), 409
    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as e:
        return render_template('signIn.html')

