#tests/test_users.py

import sys
import unittest
import json
from app.views import app

class MaintenanceTrackerApiTest(unittest.TestCase):

    def setUp(self):
        self.app = app 
        # config_name="testing"
        self.client = self.app.test_client
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