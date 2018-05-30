#app/__init__.py
#!flask/bin/python


from flask import Flask,request,jsonify,abort
from flask import make_response
# from instance.config import app_config

app = Flask(__name__)

#Initialize application
# def create_app(config_name):
#     app = FlaskAPI(__name__,instance_relative_config=True)
#     app.config.from_object(app_config[config_name])
#     app.config.from_pyfile('config.py')

#     return app

requests = [

    		{
    		'id': 1,
            'title': 'Computer will not start',
            'description': 'The computer beeps three times then goes off',
            'type': 'repair'
    		},
    		
    		{
    		'id': 2,
            'title': 'Access to the data centre',
            'description': 'There are updates that need to be installed on the servers',
            'type': 'maintenance'
    		},

    		{
    		'id': 3,
            'title': 'Computer keyboard not working',
            'description': 'I acidentally poured coffee on my keyboard',
            'type': 'repair'
    		}

    		]

@app.route('/maintenanceTrackerApp/api/v1/requests', methods=['GET'])
def get_requests():

    return jsonify({'requests':requests})

@app.route('/maintenanceTrackerApp/api/v1/requests/<int:request_id>', methods=['GET'])
def get_request(request_id):
    	request = [request for request in requests if request['id']==request_id]
    	if len(request) == 0:
    		abort(404)
    	return jsonify({'request':request[0]})

# @app.errorhandler(404)
# def request_not_found(error):
#     	return make_response(jsonify({'error':'Not found'}),404)  

@app.route('/maintenanceTrackerApp/api/v1/requests', methods=['POST'])
def create_request():   
    	if not request.json or not 'title' in request.json:
    		abort(400)

    	app_request = {

    				'id': requests[-1]['id'] + 1,
    				'title': request.json['title'],
    				'description': request.json['description'],
    				'type':request.json['type']
    	
    				}	
    	requests.append(app_request)
    	return jsonify({'app_request':app_request}),201		


@app.route('/maintenanceTrackerApp/api/v1/requests/<int:request_id>', methods=['PUT'])
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

@app.route('/maintenanceTrackerApp/api/v1/requests/<int:request_id>', methods=['DELETE'])
def delete_task(request_id):
    	request = [request for request in requests if request['id']==request_id]    	
    	if len(request) == 0:
        	abort(404)
    	request.remove(request[0])
    	return jsonify({'result': True})	

if __name__ == '__main__':
	app.run(debug=True)
