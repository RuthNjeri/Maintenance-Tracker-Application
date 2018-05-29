#test_api-tracker.py
from app import app
import unittest
import json


#The class containing the testcases of the api
class MaintenanceTrackerApiTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.request = {

                        'id': 1,
                        'title':'Computer Shut down',
                        'description':'The computer beeped three times then shuts down',
                        'type':'maintenance'  
                        
                        }

    def test_create_request(self):
        """
        Test that a user can create a request
        """
        resource = self.app.post('/users/requests/', data=self.request)
        self.assertEqual(resource.status_code,201)
        self.assertIn(self.request,str(resource.data))

    def test_read_request(self):
        """
        Test that a user can read all their requests or 
        get back an empty dictionary if they do not have requests
        """
        resource = self.app.post('/users/requests/',data=self.request)
        self.assertEqual(resource.status_code,201)
        resource = self.app.get('/users/requests/')
        self.assertEqual(resource.status_code,200)
        self.assertIn(self.request,dict(resource.data))

    def test_read_empty_request(self):
        """
        Return an empty dictionary if requests are empty
        """
        resource = self.app.post('/users/requests/',data={})
        self.assertEqual(resource.status_code,201)
        self.assertIn(self.request,dict(resource.data))
        resource = self.app.get('/users/requests/')
        self.assertEqual(resource.status_code,200)
        self.assertIn(self.request,dict(resource.data))
 

    def test_read_request_with_id(self):
        """
        Test that a user request is returned
        when the request ID is specified
        """    
        resource = self.app.post('/users/requests/',data=self.request)
        self.assertEqual(resource.status_code,201)
        json_result = json.loads(resource.data.decode())
        resource = self.app.get('/users/requests/{}'.format(json_result['id']))
        self.assertEqual(resource.status_code,200)
        self.assertIn(self.request,dict(resource.data))

    def test_no_request_with_id(self):
        """
        Test that a user request is not returned
        when the request ID is specified
        """ 
        resource = self.app.get('/users/requests/1')
        self.assertEqual(resource.status_code,404)


    def test_update_requests(self):
        """
        Test that a request can be modified
        """
        resource = self.app.post('/users/requests/',data=self.request)
        self.assertEqual(resource.status_code,201)
        json_result = json.loads(resource.data.decode())
        resource = self.app.put(
                                '/users/requests/{}'.format(json_result['id']),
                                data = {
                                        'id': 1,
                                        'title':'Computer Shuts down randomly',
                                        'description':'The computer beeped three times then shuts down',
                                        'type':'maintenance' 

                                        }
                                )
        self.assertEqual(resource.status_code,200)
        resource =self.app.get(
                                '/users/requests/{}'.format(json_result['id'])
                                )
        self.assertNotEqual(self.request['title'],resource['title'])

    def test_update_on_request_not_existing(self): 
        resource = self.app.put(
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
        resource = self.app.post('/users/requests/',data=self.request)
        self.assertEqual(resource.status_code,201)
        json_result = json.loads(resource.data.decode())
        resource = self.app.delete('/users/requests/{}'.format(json_result['id']))
        resource = self.app.get('/users/requests/{}'.format(json_result['id']))
        self.assertEqual(resource.status_code,404)

    def test_delete_request_not_existing(self):
        resource = self.app.delete('/users/requests/5')  
        self.assertEqual(resource.status_code,404)
        



if __name__ == "__main__":
    unittest.main()        

