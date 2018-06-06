#  #app/requests/views.py

#imports
from flask import Flask,request,jsonify,abort,make_response,Blueprint


#configure blueprint
requests = Blueprint('requests',__name__,template_folder='templates')

users_list = []
session = []
logged_in = ""
requests_list =[]

@requests.errorhandler(404)
def request_not_found(error):
        return make_response(jsonify({'error':'Not found'}),404)  

@requests.route('/api/v1/requests', methods=['POST'])
def create_request():   
        if not request.json or not 'title' in request.json:
            abort(400)   
        app_request = {

                        'id': len(requests_list)+1,
                        'email':request.json['email'],
                        'title': request.json['title'],
                        'description': request.json['description'],
                        'type':request.json['type']
            
                        }
        requests_list.append(app_request)

        return jsonify({'app_request':app_request}),201

"""logged in user create request
    """
@requests.route('/api/v1/users/request', methods=['POST'])    
def logged_in_user_create_request():
    if logged_in:
        app_request = {
                        'email':logged_in,
                        'id': len(session)+1,
                        'title': request.json['title'],
                        'description': request.json['description'],
                        'type':request.json['type']
            
                        }
        session.append(app_request)
        return jsonify({'Request':"Created"}),201 
    return jsonify({'request':'not created'}),404

@requests.route('/api/v1/users/requests/<int:request_id>', methods=['GET'])
def loggedin_user_get_request_id(request_id):
    if logged_in:
        request = [request for request in session if request['id']==request_id
                    and request['email']==logged_in
                    ]
        if len(requests_list) == 0:
            abort(404)
        return jsonify({'request':request[0]}),200
    return jsonify({'request':'not found'}),404                

@requests.route('/api/v1/requests/', methods=['GET'])
def logged_in_user_get_request():
    if logged_in:
        request = [request for request in session if request['email']==logged_in]
        return jsonify({'request':request}),200
    return jsonify({'request':'no requests'}),404


@requests.route('/api/v1/requests/<int:request_id>', methods=['PUT'])
def update_request(request_id):
    if logged_in:
        update_request = [request for request in session if request['id']==request_id]
        if len(update_request) == 0:
            abort(404)

        if not request.json:
            abort(400)  

        update_request[0]['title'] = request.json.get('title', update_request[0]['title'])
        update_request[0]['description'] = request.json.get('description', update_request[0]['description'])
        update_request[0]['type'] = request.json.get('type', update_request[0]['type'])
        return jsonify({'update_request': update_request[0]})   
    return jsonify({'request':'not found'}),404    

@requests.route('/api/v1/requests/<int:request_id>', methods=['DELETE'])
def delete_task(request_id):
    if logged_in:
        request = [request for request in session if request['id']==request_id]        
        if len(request) == 0:
            abort(404)
        session.remove(request[0])
        return jsonify({'message': 'Successfully deleted' })      