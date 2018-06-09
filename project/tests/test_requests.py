# tests/test_requests.py

# imports
import unittest
import sys
import json
from flask import Flask, Blueprint
from project import app
from project.users.views import jwt_auth_encode, decode_auth_token
from project.requests.views import trackerapp
from project.users.views import users, decode_auth_token
from migration import migration


class Test_requests(unittest.TestCase):
    def setUp(self):
        """
        setup migration to test requests
        """
        migration()
        self.app = app
        self.client = self.app.test_client

        """
        create user
        """
        resource = self.client().post('api/v2/auth/signup', data=json.dumps(dict(email='b@gmail.com', first_name='james', last_name='doe', password='12345678', confirm_password='12345678'
                                                                                 )), content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['response'], 'user created successfully')
        """
        login user
        """
        resource_login = self.client().post('api/v2/auth/login', data=json.dumps(dict(email="b@gmail.com", password="12345678"
                                                                                      )), content_type='application/json')
        data = json.loads(resource_login.data.decode())
        self.assertTrue(data['token'])
        self.assertEqual(decode_auth_token(data['token']), 2)
        self.assertEqual(resource_login.status_code, 200)
        self.assertEqual(resource_login.content_type, 'application/json')
        self.assertEqual(data['response'], 'login successful')
        self.headers = {'content-type': 'application/json','token': data['token']}

        """
        Create request
        """
        self.request_resource = self.client().post('/api/v2/users/requests', data=json.dumps(dict(title="Computer cannot start", description="It beeps twice when powered", request_type="repair"
                                                                                                  )), headers=self.headers)
        data = json.loads(self.request_resource.data.decode())
        self.assertEqual(self.request_resource.status_code, 201)
        self.assertEqual(data['response'], 'request created successfully')

        """
        Log in admin user
        """
        resource_login = self.client().post('api/v2/auth/login', data=json.dumps(dict(email="admin@gmail.com", password="12345678"
                                                                                      )), content_type='application/json')
        data = json.loads(resource_login.data.decode())
        self.assertEqual(resource_login.content_type, 'application/json')
        self.assertEqual(data['response'], 'login successful')
        self.admin_headers = {
            'content-type': 'application/json', 'token': data['token']}

    def test_user_create_request(self):
        """
        create request
        """
        request_resource = self.client().post('/api/v2/users/requests', data=json.dumps(dict(title="Monitor cannot start", description="something is wrong", request_type="repair"
                                                                                             )), headers=self.headers)
        data = json.loads(request_resource.data.decode())
        self.assertEqual(request_resource.content_type, 'application/json')
        self.assertEqual(data['response'], 'request created successfully')
        self.assertEqual(request_resource.status_code, 201)

    def test_user_create_existing_request(self):
        """
        test that a user cannot create an already existing request
        """
        request_resource = self.client().post('/api/v2/users/requests', data=json.dumps(dict(title="Computer cannot start", description="It beeps twice when powered", request_type="repair"
                                                                                             )), headers=self.headers)
        data = json.loads(request_resource.data.decode())
        self.assertEqual(request_resource.status_code, 409)
        self.assertEqual(request_resource.content_type, 'application/json')
        self.assertEqual(data['response'], 'request already exists')

    def test_user_get_all_requests(self):
        """
        test that a user can get all their requests
        """
        request_resource = self.client().get(
            '/api/v2/users/requests', headers=self.headers)
        data = json.loads(request_resource.data.decode())
        requests = data['requests'][0]
        self.assertEqual(request_resource.status_code, 200)
        self.assertEqual(requests['title'], "Computer cannot start")
        self.assertEqual(requests['description'],
                         "It beeps twice when powered")
        self.assertEqual(requests['type'], "repair")

    def test_user_get_specific_request(self):
        """
        test user can get a specific request
        """
        request_resource = self.client().get(
            '/api/v2/users/requests/1', headers=self.headers)
        data = json.loads(request_resource.data.decode())
        requests = data['request']
        self.assertEqual(request_resource.status_code, 200)
        self.assertEqual(requests['title'], "Computer cannot start")
        self.assertEqual(requests['description'],
                         "It beeps twice when powered")
        self.assertEqual(requests['type'], "repair")
        self.assertEqual(request_resource.status_code, 200)
        """
        test that error is returned when request not existing is accessed
        """
        request_resource = self.client().get(
            '/api/v2/users/requests/4', headers=self.headers)
        self.assertEqual(request_resource.status_code, 409)

    def test_modify_request(self):
        """
        test that a user can modify a request 
        """
        request_resource = self.client().put('/api/v2/users/requests/1', data=json.dumps(dict(title="Computer cannot start", description="poured coffee accidentally on it", type="repair"
                                                                                              )), headers=self.headers)
        self.assertEqual(request_resource.status_code, 201)
        data = json.loads(request_resource.data.decode())
        self.assertEqual(data['response'], "request modified successfuly")

    def test_admin_reads_all_requests(self):
        """
        test that admin can read requests
        """
        request_resource = self.client().get(
            '/api/v2/requests/', headers=self.admin_headers)
        data = json.loads(request_resource.data.decode())
        requests = data['requests']
        print(requests[0])
        self.assertEqual(request_resource.status_code, 200)
        self.assertEqual(requests[0]['title'], "Computer cannot start")
        self.assertEqual(requests[0]['description'],
                         "It beeps twice when powered")
        self.assertEqual(requests[0]['type'], "repair")
        self.assertEqual(request_resource.status_code, 200)

    def test_only_admin_can_change_request_approve(self):
        """
        test that only the admin can approve request
        """

        resource_approve = self.client().put('api/v2/requests/1/approve',
                                             data=json.dumps(dict(status="approved")), headers=self.headers)
        self.assertEqual(resource_approve.status_code, 401)
        data = json.loads(resource_approve.data.decode())
        self.assertEqual(data['response'], "This request is only for an admin")

    def test_only_admin_can_change_request_disapprove(self):
        """
        test that only the admin can disapprove request
        """

        resource_disapprove = self.client().put('api/v2/requests/1/approve',
                                                data=json.dumps(dict(status="disapproved")), headers=self.headers)
        self.assertEqual(resource_disapprove.status_code, 401)
        data = json.loads(resource_disapprove.data.decode())
        self.assertEqual(data['response'], "This request is only for an admin")

    def test_only_admin_can_change_request_resolve(self):
        """
        test that only the admin can approve, disapprove or resolve
        """

        resource_resolve = self.client().put('api/v2/requests/1/approve',
                                             data=json.dumps(dict(status="approved")), headers=self.headers)
        self.assertEqual(resource_resolve.status_code, 401)
        data = json.loads(resource_resolve.data.decode())
        self.assertEqual(data['response'], "This request is only for an admin")

    def test_admin_can_approve_request(self):
        """
        test that only an admin can approve requests
        """
        resource_resolve = self.client().put('api/v2/requests/1/approve',
                                             data=json.dumps(dict(status="approved")), headers=self.admin_headers)
        self.assertEqual(resource_resolve.status_code, 201)
        data = json.loads(resource_resolve.data.decode())
        self.assertEqual(data['response'], "Request approved!")

    def test_admin_can_disapprove_request(self):
        """
        test that only an admin can disapprove requests
        """
        resource_resolve = self.client().put('api/v2/requests/1/disapprove',
                                             data=json.dumps(dict(status="disapproved")), headers=self.admin_headers)
        self.assertEqual(resource_resolve.status_code, 201)
        data = json.loads(resource_resolve.data.decode())
        self.assertEqual(data['response'], "Request disapproved!")

    def test_admin_can_resolve_request(self):
        """
        test that only an admin can resolve requests
        """
        resource_resolve = self.client().put('api/v2/requests/1/resolve',
                                             data=json.dumps(dict(status="resolved")), headers=self.admin_headers)
        self.assertEqual(resource_resolve.status_code, 201)
        data = json.loads(resource_resolve.data.decode())
        self.assertEqual(data['response'], "Request resolved!")

    def test_delete_request(self):
        """
        test that a user can delete a request
        """
        request_resource = self.client().delete('/api/v2/users/requests/1',headers=self.headers)
        data = json.loads(request_resource.data.decode())
        print('data', data['response'])
        self.assertEqual(request_resource.status_code, 202)
        self.assertEqual(data['response'], "the record has been successfuly deleted")



if __name__ == '__main__':
    unittest.main()
