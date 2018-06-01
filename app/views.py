 #app/views.py



from flask import Flask,request,jsonify,abort
from flask import make_response
from . import app

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



requests = []
users = []
logged_in_user = ""

@app.route('/')
def hello():
    return "hello"

@app.route('/api/v1/requests', methods=['GET'])
def get_requests():
    if len(requests) == 0:
            abort(404)

    return jsonify({'requests':requests})

@app.route('/api/v1/requests/<int:request_id>', methods=['GET'])
def get_request(request_id):
        request = [request for request in requests if request['id']==request_id]
        if len(request) == 0:
            abort(404)
        return jsonify({'request':request[0]})

@app.errorhandler(404)
def request_not_found(error):
        return make_response(jsonify({'error':'Not found'}),404)  

@app.route('/api/v1/requests', methods=['POST'])
def create_request():   
        if not request.json or not 'title' in request.json:
            abort(400)   
        app_request = {

                        'id': len(requests)+1,
                        'title': request.json['title'],
                        'description': request.json['description'],
                        'type':request.json['type']
            
                        }
        requests.append(app_request)

        return jsonify({'app_request':app_request}),201     


@app.route('/api/v1/requests/<int:request_id>', methods=['PUT'])
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

@app.route('/api/v1/requests/<int:request_id>', methods=['DELETE'])
def delete_task(request_id):
        request = [request for request in requests if request['id']==request_id]        
        if len(request) == 0:
            abort(404)
        request.remove(request[0])
        return jsonify({'message': 'Successfully deleted' })    


@app.route('/api/v1/users/', methods=['POST'])
def create_user():
   
        
    app_request = {

                        'id': len(users)+1,
                        'email': request.json['email'],
                        'password': request.json['password'],

            
                        }
    users.append(app_request)


    return jsonify({'app_request':app_request}),201     

@app.route('/api/v1/users/login', methods=['POST'])
def login_user():

    email = request.json['email']
    password = request.json['password']

    for u in users:
        if u['email'] == email and u['password'] == password:
            logged_in_user = email
            return jsonify({'logged_in': True}) 
    return jsonify({'logged_in': False})         
