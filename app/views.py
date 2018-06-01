<<<<<<< HEAD
 #app/views.py

=======
# #app/views.py
# #!flask/bin/python
>>>>>>> 2ddb97ca05298ac7af2558e95407c1ec86a0dfb5


from flask import Flask,request,jsonify,abort
from flask import make_response
<<<<<<< HEAD
from . import app

=======
from app   import app
>>>>>>> 2ddb97ca05298ac7af2558e95407c1ec86a0dfb5
# """
#             Sample of requests
#             {
#             'id': 1,
#             'title': 'Computer will not start',
#             'description': 'The computer beeps three times then goes off',
#             'type': 'repair'
#             },
            
#             {
#             'id': 2,
#             'title': 'Access to the data centre',
#             'description': 'There are updates that need to be installed on the servers',
#             'type': 'maintenance'
#             },

#             {
#             'id': 3,
#             'title': 'Computer keyboard not working',
#             'description': 'I acidentally poured coffee on my keyboard',
#             'type': 'repair'
#             }
#             """
<<<<<<< HEAD



requests = []
users = []
logged_in_user = ""

@app.route('/')
def hello():
    return "hello"

@app.route('/api/v1/requests', methods=['GET'])
=======
requests = []
users = []


@app.route('/maintenanceapp/api/v1/requests', methods=['GET'])
>>>>>>> 2ddb97ca05298ac7af2558e95407c1ec86a0dfb5
def get_requests():

    return jsonify({'requests':requests})

<<<<<<< HEAD
@app.route('/api/v1/requests/<int:request_id>', methods=['GET'])
=======
@app.route('/maintenaneapp/api/v1/requests/<int:request_id>', methods=['GET'])
>>>>>>> 2ddb97ca05298ac7af2558e95407c1ec86a0dfb5
def get_request(request_id):
        request = [request for request in requests if request['id']==request_id]
        if len(request) == 0:
            abort(404)
        return jsonify({'request':request[0]})

@app.errorhandler(404)
def request_not_found(error):
        return make_response(jsonify({'error':'Not found'}),404)  

<<<<<<< HEAD
@app.route('/api/v1/requests', methods=['POST'])
=======
@app.route('/maintenanceapp/api/v1/requests', methods=['POST'])
>>>>>>> 2ddb97ca05298ac7af2558e95407c1ec86a0dfb5
def create_request():   
        if not request.json or not 'title' in request.json:
            abort(400)
        if len(requests)==0:    
            app_request = {

<<<<<<< HEAD
                        'id': request.json['id']+1,
=======
                        'id': request.json['id'],
>>>>>>> 2ddb97ca05298ac7af2558e95407c1ec86a0dfb5
                        'title': request.json['title'],
                        'description': request.json['description'],
                        'type':request.json['type']
            
                        }
            requests.append(app_request)
        else:   
            app_request = {

                    'id': requests[-1]['id'] + 1,
                    'title': request.json['title'],
                    'description': request.json['description'],
                    'type':request.json['type']
        
                    }   
                        
            requests.append(app_request)

        return jsonify({'app_request':app_request}),201     


<<<<<<< HEAD
@app.route('/api/v1/requests/<int:request_id>', methods=['PUT'])
=======
@app.route('/maintenanceapp/api/v1/requests/<int:request_id>', methods=['PUT'])
>>>>>>> 2ddb97ca05298ac7af2558e95407c1ec86a0dfb5
def update_request(request_id):
        update_request = [request for request in requests if request['id']==request_id]
        if len(update_request) == 0:
            abort(404)

        if not request.json:
            abort(400)  

        update_request[0]['title'] = request.json.get('title', update_request[0]['title'])
        update_request[0]['description'] = request.json.get('description', update_request[0]['description'])
        update_request[0]['type'] = request.json.get('type', update_request[0]['type'])
        return jsonify({'update_request': update_request[0]})   

<<<<<<< HEAD
@app.route('/api/v1/requests/<int:request_id>', methods=['DELETE'])
=======
@app.route('/maintenanceapp/api/v1/requests/<int:request_id>', methods=['DELETE'])
>>>>>>> 2ddb97ca05298ac7af2558e95407c1ec86a0dfb5
def delete_task(request_id):
        request = [request for request in requests if request['id']==request_id]        
        if len(request) == 0:
            abort(404)
        request.remove(request[0])
<<<<<<< HEAD
        return jsonify({'message': 'Successfully deleted' })    


@app.route('/api/v1/users/', methods=['POST'])
def create_user():
   
        
    app_request = {

                        'id': len(users)+1,
=======
        return jsonify({'result': True})    


@app.route('/maintenanceapp/api/v1/users/', methods=['POST'])
def create_user():
    if len(users)==0:
        
            app_request = {

                        'id': request.json['id'],
>>>>>>> 2ddb97ca05298ac7af2558e95407c1ec86a0dfb5
                        'email': request.json['email'],
                        'password': request.json['password'],

            
                        }
<<<<<<< HEAD
    users.append(app_request)


    return jsonify({'app_request':app_request}),201     

@app.route('/api/v1/users/login', methods=['POST'])
=======
            requests.append(app_request)
    else:

            app_request = {

                    'id': users[-1]['id'] + 1,
                    'title': request.json['email'],
                    'password': request.json['password'],

        
                    }   
                        
            requests.append(app_request)

    return jsonify({'app_request':app_request}),201     

@app.route('/maintenanceapp/api/v1/users/login', methods=['POST'])
>>>>>>> 2ddb97ca05298ac7af2558e95407c1ec86a0dfb5
def login_user():

    email = request.json['email']
    password = request.json['password']

    for u in users:
<<<<<<< HEAD
        if u['email'] == email and u['password'] == password:
            logged_in_user = email
            return jsonify({'logged_in': True}) 
    return jsonify({'logged_in': False})         
=======
        if users[u]['email'] == email and users[u]['password'] == password:
            return jsonify({'logged_in': True}) 
    return jsonify({'logged_in': False})         


>>>>>>> 2ddb97ca05298ac7af2558e95407c1ec86a0dfb5
