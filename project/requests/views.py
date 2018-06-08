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

@trackerapp.route('/users/requests',methods = ['POST'])
def user_create_request():

    token = get_token()
    try:
        if token:
            user = decode_auth_token(token)
            form = request.get_json()
            title = form['title']
            description = form['description']
            request_type = form['type']
            status = form['status']

            if title == "":
                return jsonify({'Response': 'Title cannot be empty'}),400
            if description == "":
                return jsonify({'Response':'Description cannot be empty'}),400
            #check if the request exists
            cur.execute("SELECT * FROM requests WHERE userid = %s and title = %s ;", (user, title))
            id = cur.fetchone()
            if id == None:
                date = datetime.datetime.utcnow().strftime('%Y-%m-%d')
                create_request = """INSERT INTO
                 requests  (title, description, trackertype, status, feedback, datecreated,userid)
                 VALUES ('%s','%s','%s','%s', '%s', '%s', '%s')""" % \
                 (title, description, request_type, status,'no feedback', date, user)
                cur.execute(create_request)
                conn.commit()
                return jsonify({'Response': 'request created successfully'}),201

            else:
                return jsonify({'Response': 'Request already exists'}),409

        else:
            return jsonify({'Response':'You do not have a token, try logging in again'}),401  

    except Exception as e:
        print('e',e)
        return jsonify({'Response': 'Something is wrong with your token, try logging in'}),401

@trackerapp.route('/users/requests', methods = ['GET'] )
def get_user_requests():

    token = get_token()
    try:
        if token:
            user = decode_auth_token(token)
            cur.execute("SELECT * FROM requests WHERE userid = %s;", [user])
            requests = cur.fetchall()
            if requests:
                return jsonify({'Requests': requests}),200
            else:
                return jsonify({'Requests': 'You do not have any requests'}),409
        else:
            return jsonify({'Response':'You do not have a token, try logging in again'}),401  

    except Exception as e:
        print('e',e)
        return jsonify({'Response': 'Something is wrong with your token, try logging in'}),401

@trackerapp.route('/users/requests/<int:requestId>', methods = ['GET'])
def get_specific_user_request(requestId):

    token = get_token()
 
    try:
        if token:
            user = decode_auth_token(token)
            cur.execute("SELECT * FROM requests WHERE userid = %s and id = %s ;", (user, requestId))
            get_request = cur.fetchone()
            if get_request is None:
                return jsonify({'Response':'Request does not exist'}),409
            else:
                return jsonify({'Request': get_request}),200
        else:
            return jsonify({'Response':'You do not have a token, try logging in again'}),401  

    except Exception as e:
        print('e',e)
        return jsonify({'Response': 'Something is wrong with your token, try logging in'}),401

@trackerapp.route('/users/requests/<int:requestId>', methods = ['PUT'])
def modify_user_request(requestId):
    token = get_token()
 
    try:
        if token:
            user = decode_auth_token(token)
            cur.execute("SELECT * FROM requests WHERE userid = %s and id = %s ;", (user, requestId))
            get_request = cur.fetchone()
            if get_request is None:
                return jsonify({'Response':'Request does not exist'}),409
            elif get_request[4] == 'approved':
                return jsonify({'Response':'Cannot modify request'}),401
            else:
                form = request.get_json()
                title = form['title']
                description = form['description']
                request_type = form['type']
                status = form['status']
                if title == "":
                    return jsonify({'Response': 'Title cannot be empty'}),400
                if description == "":
                    return jsonify({'Response':'Description cannot be empty'}),400
                #check if the request exists
                cur.execute("SELECT * FROM requests WHERE userid = %s and id = %s ;", (user, requestId))
                id = cur.fetchone()
                if id[1] != title or id[2] != description:
                    date = datetime.datetime.utcnow().strftime('%Y-%m-%d')
                    cur.execute("UPDATE requests SET title=%s, description=%s, trackertype=%s , status=%s WHERE id=%s;",(title, description, request_type, status, requestId))
                    conn.commit()
                    return jsonify({'Response': 'request modified successfully'}),201
                else:
                    return jsonify({'Response':'Cannot modify request, either change the title or description'}), 401

        else:
            return jsonify({'Response':'You do not have a token, try logging in again'}),401

    except Exception as e:
        print('e',e)
        return jsonify({'Response': 'Something is wrong with your token, try logging in'}),401

@trackerapp.route('/requests/', methods = ['GET'])
def admin_read_requests():
    token = get_token()
    try:
        if token:
            user = decode_auth_token(token)
            cur.execute("SELECT * FROM users WHERE id = %s and role = %s;", (user, 1))
            users = cur.fetchone()
            if users:
                cur.execute("SELECT * FROM requests")
                requests = cur.fetchall()
                if len(requests) == 0:
                    return jsonify({'Requests': 'No requests available'}),409
                else:
                    return jsonify({'Requests': requests}),200
            else:
                return jsonify({'Requests': 'Admin request only'}),401
        else:
            return jsonify({'Response':'You do not have a token, try logging in again'}),401  

    except Exception as e:
        print('e',e)
        return jsonify({'Response': 'Something is wrong with your token, try logging in'}),401

@trackerapp.route('/requests/<requestId>/approve', methods = ['PUT'])
def admin_approve_request(requestId):
    token = get_token()
    try:
        if token:
            user = decode_auth_token(token)
            cur.execute("SELECT * FROM users WHERE id = %s and role = %s;", (user, 1))
            users = cur.fetchone()
            if users:
                form = request.get_json()
                status = form ['status']
                cur.execute("SELECT * FROM requests WHERE id = %s ;", (requestId))
                requests = cur.fetchone()
                if len(requests) != 0:
                    if requests[4] == 'pending':
                        cur.execute("UPDATE requests SET status=%s WHERE id=%s;",(status,requestId))
                        conn.commit()
                        return jsonify({'Response': 'Request approved!'}),201
                    else:
                        return jsonify({'Response':'Status of the request is not pending'}),401
                else:
                    return jsonify({'Response': 'Request not found'}),409
            else:
                return jsonify({'Response':'This request is only for an admin'}),401

    except Exception as e:
        print('e',e)
        return jsonify({'Response': 'Something is wrong with your token, try logging in'}),401

@trackerapp.route('/requests/<requestId>/disapprove', methods = ['PUT'])
def disapprove_request(requestId):
    token = get_token()
    try:
        if token:
            user = decode_auth_token(token)
            cur.execute("SELECT * FROM users WHERE id = %s and role = %s;", (user, 1))
            users = cur.fetchone()
            if users:
                form = request.get_json()
                status = form ['status']
                cur.execute("SELECT * FROM requests WHERE id = %s ;", (requestId))
                requests = cur.fetchone()
                if len(requests) != 0:
                    if requests[4] != 'disapprove':
                        cur.execute("UPDATE requests SET status=%s WHERE id=%s;",(status,requestId))
                        conn.commit()
                        return jsonify({'Response': 'request disapproved!'}),201
                    else:
                        return jsonify({'Response':'Request already disapproved!'}),409
                else:
                    return jsonify({'Response': 'Request not found'}),409
            else:
                return jsonify({'Response':'This request is only for an admin'}),401

    except Exception as e:
        print('e',e)
        return jsonify({'Response': 'Something is wrong with your token, try logging in'}),401


@trackerapp.route('/requests/<requestId>/resolve', methods = ['PUT'])
def resolve_request(requestId):
    token = get_token()
    try:
        if token:
            user = decode_auth_token(token)
            cur.execute("SELECT * FROM users WHERE id = %s and role = %s;", (user, 1))
            users = cur.fetchone()
            if users:
                form = request.get_json()
                status = form ['status']
                cur.execute("SELECT * FROM requests WHERE id = %s ;", (requestId))
                requests = cur.fetchone()
                if len(requests) != 0:
                    if requests[4] != 'resolve':
                        cur.execute("UPDATE requests SET status=%s WHERE id=%s;",(status,requestId))
                        conn.commit()
                        return jsonify({'Response': 'Request resolved!'}),201
                    else:
                        return jsonify({'Response':'Request already resolved!'}),409
                else:
                    return jsonify({'Response': 'Request not found'}),409
            else:
                return jsonify({'Response':'This request is only for an admin'}),401

    except Exception as e:
        print('e',e)
        return jsonify({'Response': 'Something is wrong with your token, try logging in'}),401







