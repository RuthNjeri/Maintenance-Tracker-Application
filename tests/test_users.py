#tests/test_users.py
import unittest
import sys
import unittest
import json
from app.views import app

class MaintenanceTrackerApiTest(unittest.TestCase):
    def setUp(self):
        self.app = app 
        # config_name="testing"
        self.client = self.app.test_client
                                   
    def test_user_signup_signin(self):
        """
        Test if user is created successfully through the endpoint
        """                       
        resource = self.client().post('/api/v1/users/',data=json.dumps      
                                                        ({
                                                            'id': 1,  
                                                            'email': 'jan@gmail.com',
                                                            'password':'1234'
                                                         })
                                                            ,content_type='application/json')
        self.assertEqual(resource.status_code,201)
        """
        Test if can sign in
        """                       
        resource = self.client().post('/api/v1/users/login',data=json.dumps({
                                                                            'email':'jan@gmail.com',
                                                                            'password':'1234'
                                                                            })
                                        ,content_type='application/json')
        self.assertEqual(resource.status_code,200)

    def test_user_signup_signin_wrong_credentials(self):
        """
        Test if user is created successfully through the endpoint
        """                       
        resource = self.client().post('/api/v1/users/',data=json.dumps
                                                    ({
                                                      'id': 1,  
                                                      'email': 'jan@gmail.com',
                                                      'password':'1234'  
                                                      })
                                                    ,content_type='application/json')
        self.assertEqual(resource.status_code,201)
        """
        Test if user with wrong password credentials can sign in
        """                       
        resource = self.client().post('/api/v1/users/login',data=json.dumps({
                                                                            'email':'jan@gmail.com',
                                                                            'password':'123'
                                                                            })
                                        ,content_type='application/json')
        self.assertEqual(resource.status_code,400)
        """
        Test if user with wrong email credentials can sign in
        """   
        resource = self.client().post('/api/v1/users/login',data=json.dumps({
                                                                            'email':'j@gmail.com',
                                                                            'password':'1234'
                                                                            })
                                        ,content_type='application/json')
        self.assertEqual(resource.status_code,400)

    def test_user_not_signup_can_signin(self):
        """
        Test if user not signed up can sign in
        """                       
        resource = self.client().post('/api/v1/users/login',data=json.dumps({
                                                                            'email':'jan@gmail.com',
                                                                            'password':'123'
                                                                            })
                                        ,content_type='application/json')
        self.assertEqual(resource.status_code,400)








        

if __name__ == "__main__":
    unittest.main()             