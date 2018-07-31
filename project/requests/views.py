# # project/requests/views.py

# imports
import datetime
import psycopg2
from flask import request, jsonify, abort, Blueprint
from project.database import *
from project.users.views import decode_auth_token


# configure blueprint
trackerapp = Blueprint('trackerapp', __name__, template_folder='templates')


def expired_token():
    """
    Check if a user is using an expired token
    """
    token = request.headers.get('token', None)
    token_found = get_token(token)
    if token_found:
        return token_found


def get_user_id():
    """
    get the user id from the token
    """
    token = request.headers.get('token', None)
    user_id = decode_auth_token(token)
    if not user_id:
        return abort(401)
    return user_id


@trackerapp.app_errorhandler(404)
def request_not_found(error):
    """
    response when resquest is made to endpoints not existing
    """
    return jsonify({'response': 'Request not found'}), 404


@trackerapp.route('/users/requests', methods=['POST'])
def user_create_request():
    """
    endpoint to create a user request
    """
    token = expired_token()
    user_id = get_user_id()
    form = request.get_json()
    title = form['title']
    description = form['description']
    request_type = form['request_type']

    """
    Validate user response
    """
    if title == "" or title == " ":
        return jsonify({'response': 'Title cannot be empty'}), 400
    if description == "":
        return jsonify({'response': 'Description cannot be empty'}), 400
    """
    Check if the request exists
    """
    try:
        if token is None:
            create = Request(title, description, request_type)
            create.request_exists(user_id)
            if create.request is None:
                date_created = datetime.datetime.utcnow().strftime('%Y-%m-%d')
                create.create_request(date_created, user_id)
                return jsonify({'response':
                                'request created successfully'}), 201
            else:
                return jsonify({'response': 'request already exists'}), 409
        else:
            return jsonify({'response': 'Token invalid, log in again'}), 409

    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as e:
        print('error', e)
        return jsonify({'error': 'could not create request'}), 400


@trackerapp.route('/users/requests', methods=['GET'])
def get_users_requests():
    """
    endpoint to get all the requests of a user
    """
    token = expired_token()
    user_id = get_user_id()
    """
    get the requests of the user from the database
    """
    try:
        if token is None:
            requests = get_user_requests(user_id)
            if requests:
                return jsonify({'requests': requests}), 200
            else:
                return jsonify({'requests':
                                'You do not have any requests'}), 409
        else:
            return jsonify({'response': 'Token invalid, log in again'}), 409
    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as e:
        print('error', e)
        return jsonify({'error': 'could not get requests'}), 400


@trackerapp.route('/users/requests/<requestId>', methods=['GET'])
def get_specific_user_request(requestId):
    """
    endpoint to return a specific user request
    """
    token = expired_token()
    user_id = get_user_id()
    try:
        if token is None:
            request = get_specific_request(user_id, requestId)
            if request is None:
                return jsonify({'response': 'Request does not exist'}), 409
            else:
                return jsonify({'request': request}), 200
        else:
            return jsonify({'request': 'Token invalid, log in again'})

    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as e:
        print('error', e)
        return jsonify({'error': 'could not get the request of that id'}), 409


@trackerapp.route('/users/requests/<requestId>', methods=['PUT'])
def modify_user_request(requestId):
    """
    Endpoint to modify a user request
    """
    token = expired_token()
    user_id = get_user_id()
    try:
        if token is None:
            user_request = get_specific_request(user_id, requestId)
            if user_request is None:
                return jsonify({'response': 'Request does not exist'}), 409
            elif user_request['status'] == 'approved':
                return jsonify({'response':
                                'Cannot modify already approved request'}), 401
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
                if title == "" or title == " ":
                    return jsonify({'response': 'Title cannot be empty'}), 400
                if description == "":
                    return jsonify({'response':
                                    'Description cannot be empty'}), 400
                """
                if request details have changed
                """
                if user_request['title'] != title or \
                   user_request['description'] != description:
                    date = datetime.datetime.utcnow().strftime('%Y-%m-%d')
                    update_request(title, description,
                                   request_type, requestId, date)
                    return jsonify({'response':
                                    'request modified successfuly'}), 201
                else:
                    return jsonify({'response':
                                    'Cannot modify request,' + " " +
                                    'either change the title' + " " +
                                    'or description'}), 401
        else:
            return jsonify({'request': 'Token invalid, log in again'})

    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as e:
        print('error', e)
        return jsonify({'error': 'could not modify request of that id'}), 409


@trackerapp.route('/requests/', methods=['GET'])
def admin_read_requests():
    """
    admin endpoint to get all the requests
    """
    token = expired_token()
    print('token', token)
    user_id = get_user_id()
    try:
        if token is None:
            admin = get_admin_user(user_id)
            if admin:
                every_request = all_users_requests()
                if every_request:
                    return jsonify({'requests': every_request}), 200
                else:
                    return jsonify({'requests': 'No requests available'}), 409
            else:
                return jsonify({'requests': 'Admin request only'}), 401
        else:
            return jsonify({'request': 'Token invalid, log in again'})
    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as e:
        print('error', e)
        return jsonify({'error': 'not allowed'}), 401


@trackerapp.route('/requests/<requestId>/approve', methods=['PUT'])
def admin_approve_request(requestId):
    """
    endpoint for the admin to approve request
    """
    token = expired_token()
    user_id = get_user_id()
    try:
        if token is None:
            admin = get_admin_user(user_id)
            if admin:
                status = request_status(requestId)
                if status:
                    if status[4] == 'pending':
                        update_request_status('approved', requestId)
                        return jsonify({'response': 'Request approved!'}), 201
                    elif status[4] == 'approved':
                        return jsonify({'response':
                                        'Request already approved'}), 409
                    else:
                        return jsonify({'response':
                                        'Status of the request' + " " +
                                        'is not pending'}), 401
                else:
                    return jsonify({'response': 'Request not found'}), 409
            else:
                return jsonify({'response': 'This request is' + " " +
                                'only for an admin'}), 401
        else:
            return jsonify({'request': 'Token invalid, log in again'})

    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as e:
        print('error', e)
        return jsonify({'error': 'not allowed'}), 401


@trackerapp.route('/requests/<requestId>/disapprove', methods=['PUT'])
def disapprove_request(requestId):
    """
    endpoint for the admin to disapprove request
    """
    token = expired_token()
    user_id = get_user_id()
    try:
        if token is None:
            admin = get_admin_user(user_id)
            if admin:
                status = request_status(requestId)
                if status:
                    update_request_status('disapproved', requestId)
                    return jsonify({'response': 'Request disapproved!'}), 201
                    if status[4] == 'disapproved':
                        return jsonify({'response':
                                        'Request already disapproved'}), 409
                else:
                    return jsonify({'response': 'Request not found'}), 409
            else:
                return jsonify({'response':
                                'This request is only for an admin'}), 401
        else:
            return jsonify({'request': 'Token invalid, log in again'})
    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as e:
        print('error', e)
        return jsonify({'error': 'not allowed'}), 401


@trackerapp.route('/requests/<requestId>/resolve', methods=['PUT'])
def resolve_request(requestId):
    """
    endpoint for the admin to resolve request
    """
    token = expired_token()
    user_id = get_user_id()
    try:
        if token is None:
            admin = get_admin_user(user_id)
            if admin:
                status = request_status(requestId)
                if status:
                    update_request_status('resolved', requestId)
                    return jsonify({'response': 'Request resolved!'}), 201
                    if status[4] == 'resolved':
                        return jsonify({'response':
                                        'Request already resolved'}), 409
                else:
                    return jsonify({'response': 'Request not found'}), 409
            else:
                return jsonify({'response':
                                'This request is only for an admin'}), 401
        else:
            return jsonify({'request': 'Token invalid, log in again'})
    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as e:
        print('error', e)
        return jsonify({'error': 'not allowed'}), 401


@trackerapp.route('/auth/admin', methods=['PUT'])
def upgrade_user():
    """
    endpoint for the admin to upgrade a normal user to admin
    """
    token = expired_token()
    user_id = get_user_id()
    try:
        if token is None:
            admin = get_admin_user(user_id)
            if admin:
                form = request.get_json()
                email = form['email']
                update_user_admin(email)
                return jsonify({'response': 'User upgraded'}), 409
            else:
                return jsonify({'response': 'This request is' + " " +
                                'only for an admin'}), 401
        else:
            return jsonify({'request': 'Token invalid, log in again'})

    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as e:
        print('error', e)
        return jsonify({'error': 'not allowed'}), 401


@trackerapp.route('/users/requests/<requestId>', methods=['DELETE'])
def delete_user_request(requestId):
    """
    endpoint to return a specific user request
    """
    token = expired_token()
    user_id = get_user_id()
    try:
        if token is None:
            get_request = get_specific_request(user_id, requestId)
            if get_request is None:
                return jsonify({'response': 'Request does not exist'}), 409
            else:
                if get_request['status'] == "pending":
                    delete_request(requestId)
                    return jsonify({'response': 'the record has' + " " +
                                    'been successfuly deleted'}), 202
                else:
                    return jsonify({'response': "Cannot delete a" + " " +
                                    "record that has a status"}), 401
        else:
            return jsonify({'request': 'Token invalid, log in again'})

    except (psycopg2.DatabaseError, psycopg2.IntegrityError, Exception) as e:
        print('error', e)
        return jsonify({'error': 'could not get the request of that id'}), 409


@trackerapp.route('/signout', methods=['GET'])
def signout():
    """
    endpoint to log out user
    """
    try:
        token = request.headers.get('token')
        insert_token(token)
        return jsonify({'response': 'user logged out'})

    except Exception as e:
        print('error', e)
        return jsonify({'error': 'could not log out'}), 409
