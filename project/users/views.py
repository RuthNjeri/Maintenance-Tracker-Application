 #project/users/views.py

#imports
from flask import Flask,request,jsonify,abort,make_response,Blueprint


#configure blueprint
users = Blueprint('users',__name__,template_folder='templates')

users_list = []
session = []
logged_in = ""
requests =[]

#test if routes are working
@users.route('/')
def request():
        return "hello" 

@users.errorhandler(404)
def request_not_found(error):
        return make_response(jsonify({'error':'Not found'}),404)  



@users.route('/api/v1/users/', methods=['POST'])
def create_user():
   
        
    app_request = {

                        'id': len(users_list)+1,
                        'email': request.json['email'],
                        'password': request.json['password'],

            
                        }
    users_list.append(app_request)
    return jsonify({'app_request':app_request}),201     

@users.route('/api/v1/users/login', methods=['POST'])
def login_user():

    email = request.json['email']
    password = request.json['password']

    for u in users_list:
        if u['email'] == email and u['password'] == password:
            global logged_in
            logged_in = u['email']
            return jsonify({'logged_in': True}),200
    return jsonify({'logged_in': False}),400 

@users.route('/api/v1/users/logout')
def logout_user():
	pass

