#tests/test_users.py

import unittest
import sys
import json
from flask import Flask, Blueprint
from project.users.views import jwt_auth_encode,decode_auth_token
from project.config import conn, Config
from project import app
from project.users.views import users

class Test_users(unittest.TestCase):
    def setUp(self):
        self.app = app
        # config_name="testing"
        self.client = self.app.test_client

    def test_jwt_authentication(self):
        #create a user who is not an admin with role equal to 0 
        create_user_statement = """INSERT INTO
            users  (email,firstname,lastname,password,role)
            VALUES ('%s','%s','%s','%s', %d)""" % ("a@gmail.com","Josh","Doe","1234",0)
        #open a cursor to perform database operations
        self.cur = conn.cursor()
        self.cur.execute(create_user_statement)
        #save it in the database
        conn.commit()
        user_id_statement =("SELECT * FROM users WHERE email='a@gmail.com'")
        self.cur.execute(user_id_statement)
        results = self.cur.fetchone()
        jwt_auth_token = jwt_auth_encode(results[0])
        print('jet_auth_token ', type(jwt_auth_token))
        self.assertTrue(isinstance(jwt_auth_token,bytes))
        print('decode',decode_auth_token(jwt_auth_token))
        self.assertTrue(decode_auth_token(jwt_auth_token) == results[0])

    def test_create_users(self):
        resource = self.client().post('api/v2/auth/signup'
                                ,data= json.dumps(dict (email = 'b@gmail.com'
                                        , firstname = 'james'
                                        , lastname = 'doe'
                                        , password = '1234'
                                    )), content_type = 'application/json')
        self.assertEqual(resource.status_code,201)

    def test_create_users_who_already_exists(self):
        resource = self.client().post('api/v2/auth/signup'
                                ,data= json.dumps(dict (email = 'b@gmail.com'
                                        , firstname = 'james'
                                        , lastname = 'doe'
                                        , password = '1234'
                                    )), content_type = 'application/json')
        self.assertEqual(resource.status_code,400)


    def test_log_in(self):
        #create user
        resource_register = self.client().post('api/v2/auth/signup'
                                ,data= json.dumps(dict (email = 'd@gmail.com'
                                        , firstname = 'jackline'
                                        , lastname = 'doe'
                                        , password = '1234'
                                    )), content_type = 'application/json')
        self.assertEqual(resource_register.status_code,201)
        #login user
        resource_login =self.client().post('api/v2/auth/login',data=json.dumps(dict(email = "d@gmail.com"   
                                                                    ,password = "1234"
                                                                    )),content_type='application/json')
        data = json.loads(resource_login.data.decode())
        self.assertTrue(data['token'])
        self.assertEqual(resource_login.status_code,200)

    def test_log_in_with_wrong_password(self):
    #test if a user can log in with the wrong password
        resource_register = self.client().post('api/v2/auth/signup'
                                ,data= json.dumps(dict (email = 'x@gmail.com'
                                        , firstname = 'Tausi'
                                        , lastname = 'Tim'
                                        , password = '1234'
                                    )), content_type = 'application/json')
        self.assertEqual(resource_register.status_code,201)
        #login user with wrong password
        resource_login =self.client().post('api/v2/auth/login',data=json.dumps(dict(email = "x@gmail.com"   
                                                                    ,password = "123"
                                                                    )),content_type='application/json')
        self.assertEqual(resource_login.status_code,400)


    def test_log_in_with_wrong_email(self):
    #test if a user can log in with the wrong password
        resource_register = self.client().post('api/v2/auth/signup'
                                ,data= json.dumps(dict (email = 'pearl@gmail.com'
                                        , firstname = 'Pearl'
                                        , lastname = 'Thomas'
                                        , password = '1234'
                                    )), content_type = 'application/json')
        self.assertEqual(resource_register.status_code,201)
        #login user with wrong password
        resource_login =self.client().post('api/v2/auth/login',data=json.dumps(dict(email = "l@gmail.com"   
                                                                    ,password = "1234"
                                                                    )),content_type='application/json')
        self.assertEqual(resource_login.status_code,400)








if __name__ == '__main__':
    unittest.main()