#test_api-tracker.py

import sys
import unittest
import json
from app import create_app



#The class containing the testcases of the api
class MaintenanceTrackerApiTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app() 
        # config_name="testing"
        self.client = self.app.test_client
        self.request = {

                        'id': 1,
                        'title':'Computer Shut down',
                        'description':'The computer beeped three times then shuts down',
                        'type':'maintenance'  
                        
                        }
        self.register_user = {

                              'username':'janD',
                              'email': 'jan@gmail.com',
                              'password':'1234'  
        
                             }                

    def test_user_signup(self):
        """
        Test if user is created successfully through the endpoint
        """                       
        resource = self.client().post('/users/signup',data=self.register_user)
        self.assertEqual(resource.status_code,201)

    def test_user_signin(self):
        """
        Test if user is logged in successfully through the endpoint
        """                       
        resource = self.client().post('/users/',data=self.register_user)
        self.assertEqual(resource.status_code,201)
        resource = self.client().get('/users/')
        self.assertEqual(resource.status_code,200)   

    def test_create_request(self):
        """
        Test that a user can create a request
        """
        resource = self.client().post('/users/requests/', data=self.request)
        self.assertEqual(resource.status_code,201)
        self.assertIn(self.request,str(resource.data))

    def test_read_request(self):
        """
        Test that a user can read all their requests or 
        get back an empty dictionary if they do not have requests
        """
        resource = self.client().post('/users/requests/',data=self.request)
        self.assertEqual(resource.status_code,201)
        resource = self.client().get('/users/requests/')
        self.assertEqual(resource.status_code,200)
        self.assertIn(self.request,dict(resource.data))

    def test_read_empty_request(self):
        """
        Return an empty dictionary if requests are empty
        """
        resource = self.client().post('/users/requests/',data={})
        self.assertEqual(resource.status_code,201)
        self.assertIn(self.request,dict(resource.data))
        resource = self.client().get('/users/requests/')
        self.assertEqual(resource.status_code,200)
        self.assertIn(self.request,dict(resource.data))
 

    def test_read_request_with_id(self):
        """
        Test that a user request is returned
        when the request ID is specified
        """    
        resource = self.client().post('/users/requests/',data=self.request)
        self.assertEqual(resource.status_code,201)
        json_result = json.loads(resource.data.decode())
        resource = self.client().get('/users/requests/{}'.format(json_result['id']))
        self.assertEqual(resource.status_code,200)
        self.assertIn(self.request,dict(resource.data))

    def test_no_request_with_id(self):
        """
        Test that a user request is not returned
        when the request ID is specified
        """ 
        resource = self.client().get('/users/requests/1')
        self.assertEqual(resource.status_code,404)

    def test_read_request_with_non_existing_id(self):
        """
        Test that a user request is returned
        when the request ID is specified
        """    
        resource = self.client().get('/users/requests/9')
        self.assertEqual(resource.status_code,404)


    def test_update_requests(self):
        """
        Test that a request can be modified
        """
        resource = self.client().post('/users/requests/',data=self.request)
        self.assertEqual(resource.status_code,201)
        json_result = json.loads(resource.data.decode())
        resource = self.client().put(
                                '/users/requests/{}'.format(json_result['id']),
                                data = {
                                        'id': 1,
                                        'title':'Computer Shuts down randomly',
                                        'description':'The computer beeped three times then shuts down',
                                        'type':'maintenance' 

                                        }
                                )
        self.assertEqual(resource.status_code,200)
        resource =self.client().get(
                                '/users/requests/{}'.format(json_result['id'])
                                )
        self.assertNotEqual(self.request['title'],resource['title'])

    def test_update_on_request_not_existing(self): 
        resource = self.client().put(
                                '/users/requests/5',
                                data = {
                                        'id': 5,
                                        'title':'Computer Shuts down randomly',
                                        'description':'The computer beeped three times then shuts down',
                                        'type':'maintenance' 

                                        }
                                )  
        self.assertEqual(resource.status_code,404)                         

    def test_delete_request(self):
        resource = self.client().post('/users/requests/',data=self.request)
        self.assertEqual(resource.status_code,201)
        json_result = json.loads(resource.data.decode())
        resource = self.client().delete('/users/requests/{}'.format(json_result['id']))
        resource = self.client().get('/users/requests/{}'.format(json_result['id']))
        self.assertEqual(resource.status_code,404)

    def test_delete_request_not_existing(self):
        resource = self.client().delete('/users/requests/5')  
        self.assertEqual(resource.status_code,404)
        



if __name__ == "__main__":
    unittest.main()        

