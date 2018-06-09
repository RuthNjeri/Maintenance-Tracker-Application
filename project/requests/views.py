# # project/requests/views.py

# imports
import datetime
import jwt
import psycopg2
from flask import Flask, request, jsonify, abort, Blueprint
from project.config import Config
from project.database import Request, User
from project.users.views import decode_auth_token


# configure blueprint
trackerapp = Blueprint('trackerapp', __name__, template_folder='templates')

# create request object from Database class project/database.py

db = Request()
# create an admin user
admin = User()

def get_user_id():
    """
    get the user id from the token
    """
    token = request.headers.get('token', None)
    user_id = decode_auth_token(token)

    if not user_id:
        return abort(401)
    return user_id


@trackerapp.errorhandler(401)
def request_not_found(error):
    """
    response when resquest is made to endpoints not existing
    """
    return jsonify({'error': 'Token is invalid, login again'}), 401


@trackerapp.errorhandler(404)
def request_not_found(error):
    """
    response when resquest is made to endpoints not existing
    """
    return jsonify({'error': 'Request not found'}), 404


@trackerapp.route('/users/requests', methods=['POST'])
def user_create_request():
    """
    endpoint to create a user request
    """
    user_id = get_user_id()
    form = request.get_json()
    title = form['title']
    description = form['description']
    request_type = form['request_type']

    """
    Validate user response
    """
    if title == "":
        return jsonify({'response': 'Title cannot be empty'}), 400
    if description == "":
        return jsonify({'response': 'Description cannot be empty'}), 400
    """
    Check if the request exists
    """
    try:
        db.request_exists(user_id, title)
        if db.request is None:
            date_created = datetime.datetime.utcnow().strftime('%Y-%m-%d')
            db.create_request(title, description, request_type,
                              date_created, user_id)
            return jsonify({'response': 'request created successfully'}), 201
        else:
            return jsonify({'response': 'request already exists'}), 409

    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as e:
        return jsonify({'error': 'could not create request'}), 400


@trackerapp.route('/users/requests', methods=['GET'])
def get_user_requests():
    """
    endpoint to get all the requests of a user
    """
    user_id = get_user_id()
    """
    get the requests of the user from the database
    """
    try:
        db.get_user_requests(user_id)
        if db.requests:
            return jsonify({'requests': db.all_requests}), 200
        else:
            return jsonify({'requests': 'You do not have any requests'}), 409
    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as e:
        return jsonify({'error': 'could not get requests'}), 400

@trackerapp.route('/users/requests/<requestId>', methods=['GET'])
def get_specific_user_request(requestId):
    """
    endpoint to return a specific user request
    """
    user_id = get_user_id()
    try:
        db.get_specific_request(user_id, requestId)
        if db.request is None:
            return jsonify({'response': 'Request does not exist'}), 409
        else:
            return jsonify({'request': db.request_labeled}), 200

    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as e:
        return jsonify({'error': 'could not get the request of that id'}), 409


@trackerapp.route('/users/requests/<requestId>', methods=['PUT'])
def modify_user_request(requestId):
    """
    Endpoint to modify a user request
    """
    user_id = get_user_id()
    try:
        db.get_specific_request(user_id, requestId)
        if db.request is None:
            return jsonify({'response': 'Request does not exist'}), 409
        elif db.request_labeled['status'] == 'approved':
            return jsonify({'response': 'Cannot modify already approved request'}), 401
        else:
            """
            modify request
            """
            form = request.get_json()
            title = form['title']
            description = form['description']
            request_type = form['type']
            """
            Validate user input
            """
            if title == "":
                return jsonify({'response': 'Title cannot be empty'}), 400
            if description == "":
                return jsonify({'response': 'Description cannot be empty'}), 400
            """
            if request details have changed
            """
            if db.request_labeled['title'] != title or db.request_labeled['description'] != description:
                date = datetime.datetime.utcnow().strftime('%Y-%m-%d')
                db.update_request(title, description,
                                  request_type, requestId, date)
                return jsonify({'response': 'request modified successfuly'}), 201
            else:
                return jsonify({'response': 'Cannot modify request, either change the title or description'}), 401
    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as e:
        return jsonify({'error': 'could not modify request of that id'}), 409


@trackerapp.route('/requests/', methods=['GET'])
def admin_read_requests():
    """
    admin endpoint to get all the requests
    """
    user_id = get_user_id()
    try:
        admin.get_admin_user(user_id)
        if admin.admin:
            db.all_users_requests()
            if db.every_request:
                return jsonify({'requests': db.every_request}), 200
            else:
                return jsonify({'requests': 'No requests available'}), 409
        else:
            return jsonify({'requests': 'Admin request only'}), 401
    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as e:
        return jsonify({'error': 'not allowed'}), 401


@trackerapp.route('/requests/<requestId>/approve', methods=['PUT'])
def admin_approve_request(requestId):
    """
    endpoint for the admin to approve request
    """
    user_id = get_user_id()
    try:
        admin.get_admin_user(user_id)
        if admin.admin:
            db.request_status(requestId)
            if db.requests:
                if db.requests[4] == 'pending':
                    db.update_request_status('approved', requestId)
                    return jsonify({'response': 'Request approved!'}), 201
                if db.requests[4] == 'approved':
                    return jsonify({'response': 'Request already approved'}), 409
                else:
                    return jsonify({'response': 'Status of the request is not pending'}), 401
            else:
                return jsonify({'response': 'Request not found'}), 409
        else:
            return jsonify({'response': 'This request is only for an admin'}), 401

    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as e:
        return jsonify({'error': 'not allowed'}), 401


@trackerapp.route('/requests/<requestId>/disapprove', methods=['PUT'])
def disapprove_request(requestId):
    """
    endpoint for the admin to disapprove request
    """
    user_id = get_user_id()
    try:
        admin.get_admin_user(user_id)
        if admin.admin:
            db.request_status(requestId)
            if db.requests:
                db.update_request_status('disapproved', requestId)
                return jsonify({'response': 'Request disapproved!'}), 201
                if requests[4] == 'disapproved':
                    return jsonify({'response': 'Request already disapproved'}), 409
            else:
                return jsonify({'response': 'Request not found'}), 409
        else:
            return jsonify({'response': 'This request is only for an admin'}), 401
    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as e:
        return jsonify({'error': 'not allowed'}), 401


@trackerapp.route('/requests/<requestId>/resolve', methods=['PUT'])
def resolve_request(requestId):
    """
    endpoint for the admin to resolve request
    """
    user_id = get_user_id()
    try:
        admin.get_admin_user(user_id)
        if admin.admin:
            db.request_status(requestId)
            if db.requests:
                db.update_request_status('resolved', requestId)
                return jsonify({'response': 'Request resolved!'}), 201
                if requests[4] == 'resolved':
                    return jsonify({'response': 'Request already resolved'}), 409
            else:
                return jsonify({'response': 'Request not found'}), 409
        else:
            return jsonify({'response': 'This request is only for an admin'}), 401
    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as e:
        return jsonify({'error': 'not allowed'}), 401
