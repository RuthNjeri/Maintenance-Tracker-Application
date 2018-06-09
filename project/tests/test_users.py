# tests/test_users.py

import unittest
import sys
import json
from flask import Flask, Blueprint
from project.users.views import jwt_auth_encode, decode_auth_token
from project import app
from project.users.views import users
from project.database import User
from migration import migration



class Test_users(unittest.TestCase):
    def setUp(self):
        """
        restart migration and set up test users
        """
        migration()
        self.app = app
        self.client = self.app.test_client
        self.db = User()

    def test_jwt_authentication(self):
        """
        test if a user can be authenticated
        """
        self.db.create_user("b@gmail.com", "Josh", "Doe", "1234")
        self.db.user_email_exists("b@gmail.com")
        jwt_auth_token = jwt_auth_encode(self.db.user[0])
        self.assertTrue(isinstance(jwt_auth_token, bytes))
        self.assertTrue(decode_auth_token(jwt_auth_token) == self.db.user[0])

    def test_create_users(self):
        """
        test if a user can be created
        """
        resource = self.client().post('api/v2/auth/signup', data=json.dumps(dict(email='b@gmail.com', first_name='james', last_name='doe', password='12345678', confirm_password='12345678'
                                                                                 )), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['response'], 'user created successfully')

    def test_create_users_who_already_exists(self):
        """
        test that a user who already exists cannot be created
        """
        resource = self.client().post('api/v2/auth/signup', data=json.dumps(dict(email='sh@gmail.com', first_name='sasha', last_name='doe', password='12345678', confirm_password='12345678'
                                                                                 )), content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['response'], 'user created successfully')

        resource = self.client().post('api/v2/auth/signup', data=json.dumps(dict(email='sh@gmail.com', first_name='sasha', last_name='doe', password='12345678', confirm_password='12345678'
                                                                                 )), content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 409)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['response'], 'user already exists')

    def test_user_enters_valid_email(self):
        """
        test that an email entered is not empty
        """
        resource = self.client().post('api/v2/auth/signup', data=json.dumps(dict(email='', first_name='sasha', last_name='doe', password='12345678', confirm_password='12345678'
                                                                                 )), content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 409)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['response'], 'email cannot be empty')
        """
        test email is entered in the correct format
        """
        resource = self.client().post('api/v2/auth/signup', data=json.dumps(dict(email='sh.com', first_name='sasha', last_name='doe', password='12345678', confirm_password='12345678'
                                                                                 )), content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 409)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['response'], 'enter email in correct format')

    def test_user_enters_valid_password(self):
        """
        test that a user enters a valid password
        """
        resource = self.client().post('api/v2/auth/signup', data=json.dumps(dict(email='sh@gmail.com', first_name='sasha', last_name='doe', password='1234', confirm_password='1234'
                                                                                 )), content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 409)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['response'], 'password must be 8 values or more')

        """
        test empty password
        """

        resource = self.client().post('api/v2/auth/signup', data=json.dumps(dict(email='sh@gmail.com', first_name='sasha', last_name='doe', password='', confirm_password='12345678'
                                                                                 )), content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 409)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['response'], 'password cannot be empty')

        """
        test password not matching
        """
        resource = self.client().post('api/v2/auth/signup', data=json.dumps(dict(email='sh@gmail.com', first_name='sasha', last_name='doe', password='1234', confirm_password='12345678'
                                                                                 )), content_type='application/json')
        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 409)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['response'], 'password does not match')

    def test_log_in(self):
        """
        test that a user can log in
        """
        resource_register = self.client().post('api/v2/auth/signup', data=json.dumps(dict(email='d@gmail.com', first_name='jackline', last_name='doe', password='12345678', confirm_password='12345678'
                                                                                          )), content_type='application/json')
        data = json.loads(resource_register.data.decode())
        self.assertEqual(resource_register.status_code, 201)
        self.assertEqual(resource_register.content_type, 'application/json')
        self.assertEqual(data['response'], 'user created successfully')
        """
        log in user created
        """
        resource_login = self.client().post('api/v2/auth/login', data=json.dumps(dict(email="d@gmail.com", password="12345678"
                                                                                      )), content_type='application/json')
        data = json.loads(resource_login.data.decode())
        self.assertTrue(data['token'])
        self.assertEqual(decode_auth_token(data['token']), 2)
        self.assertEqual(resource_login.status_code, 200)
        self.assertEqual(resource_login.content_type, 'application/json')
        self.assertEqual(data['response'], 'login successful')

    def test_log_in_with_wrong_password(self):
        """
        test that a user cannot login with wrong password
        """
        resource_register = self.client().post('api/v2/auth/signup', data=json.dumps(dict(email='d@gmail.com', first_name='jackline', last_name='doe', password='12345678', confirm_password='12345678'
                                                                                          )), content_type='application/json')
        data = json.loads(resource_register.data.decode())
        self.assertEqual(resource_register.status_code, 201)
        self.assertEqual(resource_register.content_type, 'application/json')
        self.assertEqual(data['response'], 'user created successfully')
        """
        login user with wrong password
        """
        resource_login = self.client().post('api/v2/auth/login', data=json.dumps(dict(email="d@gmail.com", password=""
                                                                                      )), content_type='application/json')
        self.assertEqual(resource_login.status_code, 409)
        data = json.loads(resource_login.data.decode())
        self.assertEqual(resource_login.content_type, 'application/json')
        self.assertEqual(data['response'],
                         'Please enter the correct user details')

    def test_log_in_with_wrong_email(self):
        """
        test that a user cannot login with wrong email
        """
        resource_register = self.client().post('api/v2/auth/signup', data=json.dumps(dict(email='d@gmail.com', first_name='jackline', last_name='doe', password='12345678', confirm_password='12345678'
                                                                                          )), content_type='application/json')
        data = json.loads(resource_register.data.decode())
        self.assertEqual(resource_register.status_code, 201)
        self.assertEqual(resource_register.content_type, 'application/json')
        self.assertEqual(data['response'], 'user created successfully')
        """
        login user with wrong password
        """
        resource_login = self.client().post('api/v2/auth/login', data=json.dumps(dict(email="dee@gmail.com", password="12345678"
                                                                                      )), content_type='application/json')
        self.assertEqual(resource_login.status_code, 409)
        data = json.loads(resource_login.data.decode())
        self.assertEqual(resource_login.content_type, 'application/json')
        self.assertEqual(data['response'], 'user not found')


if __name__ == '__main__':
    unittest.main()
