#tests/test_users.py

import unittest
import sys
import json
from flask import Flask, Blueprint
from project.users.views import jwt_auth_encode,decode_auth_token
from project.config import conn, Config
from project import app
from project.requests.views import trackerapp
from project.users.views import users
from migration import migration
from project.users.views import decode_auth_token


class Test_requests(unittest.TestCase):
    def setUp(self):
        migration()
        self.app = app
        # config_name="testing"
        self.client = self.app.test_client
        self.cur = conn.cursor()


    def test_user_create_request(self):
        #create user
        resource = self.client().post('api/v2/auth/signup'
                                ,data = json.dumps(dict (email = 'joe@gmail.com'
                                        , firstname = 'shawn'
                                        , lastname = 'doe'
                                        , password = '1234'
                                    )), content_type = 'application/json')
        self.assertEqual(resource.status_code,201)
        #login user
        resource_login =self.client().post('api/v2/auth/login',data=json.dumps(dict(email = "joe@gmail.com"   
                                                                    ,password = "1234"
                                                                    )),content_type='application/json')
        data = json.loads(resource_login.data.decode())
        token = data['token']
        decode = decode_auth_token(token)
        self.assertTrue(data['token'])
        self.assertEqual(resource_login.status_code,200)
        headers = {'content-type': 'application/json', 'token':token}
        print('headers',headers)
        request_resource = self.client().post('/api/v2/users/requests'
                                            ,data = json.dumps(dict(title = "Computer cannot start"
                                                    ,description = "It beeps twice when powered"
                                                    ,type = "repair"
                                                    ,status = "pending")),headers = headers)
        self.assertEqual(request_resource.status_code,201)

    def test_user_create_existing_request(self):
        #create user
        resource = self.client().post('api/v2/auth/signup'
                                ,data = json.dumps(dict (email = 'janet@gmail.com'
                                        , firstname = 'sheen'
                                        , lastname = 'doe'
                                        , password = '1234'
                                    )), content_type = 'application/json')
        self.assertEqual(resource.status_code,201)
        #login user
        resource_login =self.client().post('api/v2/auth/login',data=json.dumps(dict(email = "janet@gmail.com"   
                                                                    ,password = "1234"
                                                                    )),content_type='application/json')
        data = json.loads(resource_login.data.decode())
        token = data['token']
        decode = decode_auth_token(token)
        self.assertTrue(data['token'])
        self.assertEqual(resource_login.status_code,200)
        headers = {'content-type': 'application/json', 'token':token}
        request_resource = self.client().post('/api/v2/users/requests'
                                            ,data = json.dumps(dict(title = "Computer cannot start"
                                                    ,description = "It beeps twice when powered"
                                                    ,type = "repair"
                                                    ,status = "pending")),headers = headers)
        self.assertEqual(request_resource.status_code,201)
        request_resource = self.client().post('/api/v2/users/requests'
                                            ,data = json.dumps(dict(title = "Computer cannot start"
                                                    ,description = "It beeps twice when powered"
                                                    ,type = "repair"
                                                    ,status = "pending")),headers = headers)
        self.assertEqual(request_resource.status_code,409)   

    def test_user_get_all_requests(self):
        #create user
        resource = self.client().post('api/v2/auth/signup'
                                ,data = json.dumps(dict (email = 'irene@gmail.com'
                                        , firstname = 'sheena'
                                        , lastname = 'doe'
                                        , password = '1234'
                                    )), content_type = 'application/json')
        self.assertEqual(resource.status_code,201)
        #login user
        resource_login =self.client().post('api/v2/auth/login',data=json.dumps(dict(email = "irene@gmail.com"   
                                                                    ,password = "1234"
                                                                    )),content_type='application/json')
        data = json.loads(resource_login.data.decode())
        token = data['token']
        decode = decode_auth_token(token)
        self.assertTrue(data['token'])
        self.assertEqual(resource_login.status_code,200)
        headers = {'content-type': 'application/json', 'token':token}
        #get requests when there are no requests by the user
        request_resource = self.client().get('/api/v2/users/requests',headers = headers)
        self.assertEqual(request_resource.status_code,409)
        #return requests when there are requests
        request_resource = self.client().post('/api/v2/users/requests'
                                            ,data = json.dumps(dict(title = "Computer cannot start"
                                                    ,description = "It beeps twice when powered"
                                                    ,type = "repair"
                                                    ,status = "pending")),headers = headers)
        self.assertEqual(request_resource.status_code,201)
        request_resource = self.client().get('/api/v2/users/requests',headers = headers)
        self.assertEqual(request_resource.status_code,200)

    def test_user_get_specific_request(self):
        #create user
        resource = self.client().post('api/v2/auth/signup'
                                ,data = json.dumps(dict (email = 'Tony@gmail.com'
                                        , firstname = 'sheena'
                                        , lastname = 'doe'
                                        , password = '1234'
                                    )), content_type = 'application/json')
        self.assertEqual(resource.status_code,201)
        #login user
        resource_login =self.client().post('api/v2/auth/login',data=json.dumps(dict(email = "Tony@gmail.com"   
                                                                    ,password = "1234"
                                                                    )),content_type='application/json')
        data = json.loads(resource_login.data.decode())
        print('data',data)
        token = data['token']
        decode = decode_auth_token(token)
        self.assertTrue(data['token'])
        self.assertEqual(resource_login.status_code,200)
        headers = {'content-type': 'application/json', 'token':token}
        #return error when request does not exist
        request_resource = self.client().get('/api/v2/users/requests/1',headers = headers)
        self.assertEqual(request_resource.status_code,409)
        #return specific request
        request_resource = self.client().post('/api/v2/users/requests'
                                            ,data = json.dumps(dict(title = "Computer cannot start"
                                                    ,description = "It beeps twice when powered"
                                                    ,type = "repair"
                                                    ,status = "pending")),headers = headers)
        self.assertEqual(request_resource.status_code,201)
        request_resource = self.client().get('/api/v2/users/requests/1',headers = headers)
        self.assertEqual(request_resource.status_code,200)

    def test_modify_request_already_approved(self):
        #create user
        resource = self.client().post('api/v2/auth/signup'
                                ,data = json.dumps(dict (email = 'jesus@gmail.com'
                                        , firstname = 'shawn'
                                        , lastname = 'doe'
                                        , password = '1234'
                                    )), content_type = 'application/json')
        self.assertEqual(resource.status_code,201)
        #login user
        resource_login =self.client().post('api/v2/auth/login',data=json.dumps(dict(email = "jesus@gmail.com"   
                                                                    ,password = "1234"
                                                                    )),content_type='application/json')
        data = json.loads(resource_login.data.decode())
        token = data['token']
        decode = decode_auth_token(token)
        self.assertTrue(data['token'])
        self.assertEqual(resource_login.status_code,200)
        headers = {'content-type': 'application/json', 'token':token}
        print('headers',headers)
        request_resource = self.client().post('/api/v2/users/requests'
                                            ,data = json.dumps(dict(title = "Computer cannot start"
                                                    ,description = "It beeps twice when powered"
                                                    ,type = "repair"
                                                    ,status = "approved")),headers = headers)
        self.assertEqual(request_resource.status_code,201)
        request_resource = self.client().put('/api/v2/users/requests/1'
                                            ,data = json.dumps(dict(title = "Computer cannot start"
                                                    ,description = "It beeps twice when powered"
                                                    ,type = "repair"
                                                    ,status = "pending")),headers = headers)
        self.assertEqual(request_resource.status_code,401)

    def test_admin_reads_all_requests(self):
        #login admin
        resource_login =self.client().post('api/v2/auth/login',data=json.dumps(dict(email = "admin@gmail.com"   
                                                                    ,password = "12345"
                                                                    )),content_type='application/json')
        data = json.loads(resource_login.data.decode())
        token = data['token']
        decode = decode_auth_token(token)
        self.assertTrue(data['token'])
        self.assertEqual(resource_login.status_code,200)
        headers = {'content-type': 'application/json', 'token':token}
        print('headers',headers)
        request_resource = self.client().get('/api/v2/requests/',headers = headers)
        #there are no requests in the database
        self.assertEqual(request_resource.status_code,409)

    def test_only_admin_can_change_request_status_approved(self):
        #create user request
        resource = self.client().post('api/v2/auth/signup'
                                ,data = json.dumps(dict (email = 'joe@gmail.com'
                                        , firstname = 'shawn'
                                        , lastname = 'doe'
                                        , password = '1234'
                                    )), content_type = 'application/json')
        self.assertEqual(resource.status_code,201)
        #login user
        resource_login =self.client().post('api/v2/auth/login',data=json.dumps(dict(email = "joe@gmail.com"   
                                                                    ,password = "1234"
                                                                    )),content_type='application/json')
        data = json.loads(resource_login.data.decode())
        token = data['token']
        decode = decode_auth_token(token)
        self.assertTrue(data['token'])
        self.assertEqual(resource_login.status_code,200)
        headers = {'content-type': 'application/json', 'token':token}
        print('headers',headers)
        request_resource = self.client().post('/api/v2/users/requests'
                                            ,data = json.dumps(dict(title = "Computer cannot start"
                                                    ,description = "It beeps twice when powered"
                                                    ,type = "repair"
                                                    ,status = "pending")),headers = headers)
        self.assertEqual(request_resource.status_code,201)
        #cannot approve request
        resource_approve = self.client().put('api/v2/requests/1/approve' 
                                                ,data = json.dumps(dict(status = "approve")), headers = headers)
        self.assertEqual(resource_approve.status_code,401)
        #cannot disapprove request
        resource_approve = self.client().put('api/v2/requests/1/approve' 
                                                ,data = json.dumps(dict(status = "disapprove")), headers = headers)
        self.assertEqual(resource_approve.status_code,401)
        #cannot resolve request
        resource_approve = self.client().put('api/v2/requests/1/approve' 
                                                ,data = json.dumps(dict(status = "resolve")), headers = headers)
        self.assertEqual(resource_approve.status_code,401)

    def test_admin_can_approve_pending_request(self):
        #login admin
        resource_login =self.client().post('api/v2/auth/login',data=json.dumps(dict(email = "admin@gmail.com"   
                                                                    ,password = "12345"
                                                                    )),content_type='application/json')
        data = json.loads(resource_login.data.decode())
        token = data['token']
        decode = decode_auth_token(token)
        self.assertTrue(data['token'])
        self.assertEqual(resource_login.status_code,200)
        headers = {'content-type': 'application/json', 'token':token}
        print('headers',headers)
        request_resource = self.client().post('/api/v2/users/requests'
                                            ,data = json.dumps(dict(title = "Computer cannot start"
                                                    ,description = "It beeps twice when powered"
                                                    ,type = "repair"
                                                    ,status = "approve")),headers = headers)
        self.assertEqual(request_resource.status_code,201)
        resource_approve = self.client().put('api/v2/requests/1/approve' 
                                                ,data = json.dumps(dict(status = "approve")), headers = headers)
        self.assertEqual(resource_approve.status_code,401)

    def test_admin_can_disapprove_request(self):
        #login admin
        resource_login =self.client().post('api/v2/auth/login',data=json.dumps(dict(email = "admin@gmail.com"   
                                                                    ,password = "12345"
                                                                    )),content_type='application/json')
        data = json.loads(resource_login.data.decode())
        token = data['token']
        decode = decode_auth_token(token)
        self.assertTrue(data['token'])
        self.assertEqual(resource_login.status_code,200)
        headers = {'content-type': 'application/json', 'token':token}
        print('headers',headers)
        request_resource = self.client().post('/api/v2/users/requests'
                                            ,data = json.dumps(dict(title = "Computer cannot start"
                                                    ,description = "It beeps twice when powered"
                                                    ,type = "repair"
                                                    ,status = "approve")),headers = headers)
        self.assertEqual(request_resource.status_code,201)
        resource_approve = self.client().put('api/v2/requests/1/disapprove' 
                                                ,data = json.dumps(dict(status = "disapprove")), headers = headers)
        self.assertEqual(resource_approve.status_code,201)

    def test_admin_can_resolve_request(self):
         #login admin
        resource_login =self.client().post('api/v2/auth/login',data=json.dumps(dict(email = "admin@gmail.com"   
                                                                    ,password = "12345"
                                                                    )),content_type='application/json')
        data = json.loads(resource_login.data.decode())
        token = data['token']
        decode = decode_auth_token(token)
        self.assertTrue(data['token'])
        self.assertEqual(resource_login.status_code,200)
        headers = {'content-type': 'application/json', 'token':token}
        print('headers',headers)
        request_resource = self.client().post('/api/v2/users/requests'
                                            ,data = json.dumps(dict(title = "Computer cannot start"
                                                    ,description = "It beeps twice when powered"
                                                    ,type = "repair"
                                                    ,status = "approve")),headers = headers)
        self.assertEqual(request_resource.status_code,201)
        resource_approve = self.client().put('api/v2/requests/1/resolve' 
                                                ,data = json.dumps(dict(status = "resolve")), headers = headers)
        self.assertEqual(resource_approve.status_code,201)














if __name__ == '__main__':
    unittest.main()