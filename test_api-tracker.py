#test_api-tracker.py

import unittest
import os
from app import app

#the testcase of the api
class MaintenanceTrackerApiTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.request = {

                        'id': 1,
                        'title':'Computer Shut down',
                        'description':'The computer beeped three times then shuts down',
                        'type':'maintenance'  
                        
                        }

    def test_post_request(self):
        resource = self.app.post('/requests/', data=self.request)
        self.assertEqual(resource.status_code,201)
        self.assertIn(self.request,str(resource.data))


if __name__ == "__main__":
    unittest.main()        

