#tests/test_users.py

import unittest
import sys
import json
from flask import Flask, Blueprint
from project.users.views import jwt_auth_encode,decode_auth_token
from project.config import conn, Config
from project import app
from project.requests.views import trackerapp

class Test_requests(unittest.TestCase):
    def setUp(self):
        self.app = app
        # config_name="testing"
        self.client = self.app.test_client









if __name__ == '__main__':
    unittest.main()