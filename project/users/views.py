# project/users/views.py

# imports
import datetime
import jwt
import psycopg2
from flask import Flask, request, jsonify, abort, make_response, Blueprint
from project.config import conn, Config





# configure blueprint
users = Blueprint('users', __name__, template_folder='templates')

cur = conn.cursor()



def jwt_auth_encode(userid):
    # to generate the auth token

    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
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
    # decode auth token
    try:
        payload = jwt.decode(auth_token,Config.SECRET)
        return payload['sub']
    except Exception as e:
        return("Try logging in again", e)

@users.route('/')
def index():
    return "hello"

@users.errorhandler(404)
def request_not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@users.route('/auth/signup', methods=['POST'])
def create_user():
    form = request.get_json()
    print('form', form)
    email = form['email']
    firstname = form['firstname']
    lastname = form['lastname']
    password = form['password']

    try:
        if email == "":
            return jsonify({'response': 'email cannot be empty'})
        if password == "":
            return jsonify({'response': 'password cannot be empty'})
        cur.execute("SELECT * FROM users WHERE email=%s and password=%s;", (email, password,))
        user = cur.fetchone()
        print('user',user)

        if user is None:
            create_user_statement = """INSERT INTO
                users  (email, firstname, lastname, password, role)
                VALUES ('%s','%s','%s','%s', %d)""" % (email, firstname, lastname, password, 0)
            cur.execute(create_user_statement)
            conn.commit()
            return jsonify({'response': 'user created successfully'}),201
        else:
            return jsonify({'response': 'user already exists'}),409

    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as e:
        return jsonify({'Response':'please enter your email, firstname, lastname and password' }),400


@users.route('/auth/login', methods=['POST'])
def login_user():
    form = request.get_json()
    email = form['email']
    password = form['password']


    try:
        cur.execute("SELECT * FROM users WHERE email=%s and password=%s;", (email, password,))
        id = cur.fetchone()
        token = jwt_auth_encode(id[0])
        if token and email:
            response = {  'message':'login successfull'
                        , 'token': token.decode()
                        }
            return jsonify(response),200
    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as e:
        print('e',e)
        return jsonify({'Response': 'Please enter the correct user details'}),409


