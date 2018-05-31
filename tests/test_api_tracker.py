#test_api-tracker.py

import sys
import unittest
import json
from app.views import app



#The class containing the testcases of the api
class MaintenanceTrackerApiTest(unittest.TestCase):

    def setUp(self):
        self.app = app 
        # config_name="testing"
        self.client = self.app.test_client
        self.request = {

                        'id': 1,
                        'title':'Computer Shut down',
                        'description':'The computer beeped three times then shuts down',
                        'type':'maintenance'  
                        
                        }
        self.request_empty ={} 
              
        self.register_user = {
                              'id': 1,  
                              'email': 'jan@gmail.com',
                              'password':'1234'  
        
                             }                

    def test_user_signup(self):
        """
        Test if user is created successfully through the endpoint
        """                       
        resource = self.client().post('/maintenanceapp/api/v1/users/',data=json.dumps(self.register_user)
                                       ,content_type='application/json')
        self.assertEqual(resource.status_code,201)

    def test_user_signin(self):
        """
        Test if user is logged in successfully through the endpoint
        """                       
        resource = self.client().post('/maintenanceapp/api/v1/users/login',data=json.dumps(self.register_user)
                                        ,content_type='application/json')
        self.assertEqual(resource.status_code,200)
  

    def test_create_request(self):
        """
        Test that a user can create a request
        """
        resource = self.client().post('/maintenanceapp/api/v1/requests', data=json.dumps(self.request)
                                        ,content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code,201)
        self.assertIn(data['app_request']['title'],self.request['title'])

    def test_read_request(self):
        """
        Test that a user can read all their requests or 
        get back an empty dictionary if they do not have requests
        """
        resource = self.client().post('/maintenanceapp/api/v1/requests', data=json.dumps(self.request)
                                         ,content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code,201)
        resource = self.client().get('/maintenanceapp/api/v1/requests')
        self.assertEqual(resource.status_code,200)
     


    def test_create_empty_request(self):
        """
        Create an empty dictionary if requests are empty
        """
        resource = self.client().post('/maintenanceapp/api/v1/requests', data=json.dumps(self.request_empty)
                                          ,content_type='application/json')
        self.assertEqual(resource.status_code,400)

 

    def test_read_request_with_id(self):
        """
        Test that a user request is returned
        when the request ID is specified.
        This test runs independently
        """    
        
        resource = self.client().post('/maintenanceapp/api/v1/requests', data=json.dumps(self.request)
                                          ,content_type='application/json')
        self.assertEqual(resource.status_code,201)
        data = json.loads(resource.data.decode())
        resource = self.client().get('/maintenaneapp/api/v1/requests/{}'.format(data['app_request']['id']))
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code,200)
        self.assertIn(data['request']['title'],self.request['title'])


    def test_no_request_with_id(self):
        """
        Test that a user request is not returned
        when the request ID is specified
        """ 
        resource = self.client().get('/maintenaneapp/api/v1/requests/100')
        self.assertEqual(resource.status_code,404)

    def test_read_request_with_non_existing_id(self):
        """
        Test that a user request is returned
        when the request ID is specified
        """    
        resource = self.client().get('/maintenaneapp/api/v1/requests/100')
        self.assertEqual(resource.status_code,404)

     
    def test_update_requests(self):
        """ Not yet working  
        Test that a request can be modified
        """
        self.request['title']='new'
        resource = self.client().post('/maintenanceapp/api/v1/requests', data=json.dumps(self.request)
                                          ,content_type='application/json')
        json_result = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code,201)
        self.assertIn(json_result['app_request']['title'],'new')

 

    def test_update_on_request_not_existing(self): 
        resource = self.client().put('/maintenanceapp/api/v1/requests/100'
                                    ,data=json.dumps(self.request)
                                    ,content_type='application/json')
                                
        self.assertEqual(resource.status_code,404)                         

    def test_delete_request(self):
        resource = self.client().post('/maintenanceapp/api/v1/requests', data=json.dumps(self.request)
                                           ,content_type='application/json')
        self.assertEqual(resource.status_code,201)
        json_result = json.loads(resource.data.decode())
        resource = self.client().delete('/maintenanceapp/api/v1/requests/{}'.format(json_result))
        resource = self.client().get('/maintenanceapp/api/v1/requests/{}'.format(json_result))
        self.assertEqual(resource.status_code,404)

    def test_delete_request_not_existing(self):
        resource = self.client().delete('/maintenaneapp/api/v1/requests/{}')  
        self.assertEqual(resource.status_code,404)
    

           





if __name__ == "__main__":
    unittest.main()        

