import psycopg2
from werkzeug.security import generate_password_hash
from project.config import conn


class Database():
    """docstring for Database"""

    def __init__(self):

        self.conn = conn
        self.cur = self.conn.cursor()

    def create_user(self, email, first_name, last_name, password):
        """"
        Create the user in the database
        """
        password_hash = generate_password_hash(password)
        create_user_statement = """INSERT INTO
                users  (email, first_name, last_name, password_hash, role)
                VALUES ('%s','%s','%s','%s', %d)""" % (email, first_name, last_name, password_hash, 0)
        self.cur.execute(create_user_statement)
        self.conn.commit()

    def user_email_exists(self, email):
        """
        Check if a user with a specific email exists in the database
        """
        self.cur.execute("SELECT * FROM users WHERE email=%s;", (email,))
        self.user = self.cur.fetchone()

    def get_admin_user(self, user_id):
        """
        query the database to see if a user is an admin
        """
        self.cur.execute(
            "SELECT * FROM users WHERE id = %s and role = %s;", (user_id, 1))
        self.admin = self.cur.fetchone()

    def request_exists(self, user_id, title):
        """
        Check if a user exists
        """
        self.cur.execute(
            "SELECT * FROM requests WHERE user_id = %s and title = %s ;", (user_id, title))
        self.request = self.cur.fetchone()

    def create_request(self, title, description, request_type, date_created, user_id):
        """
        Create user request
        """
        create_request = """INSERT INTO
                 requests  (title, description, request_type, status, feedback, date_created, user_id)
                 VALUES ('%s','%s','%s','%s', '%s', '%s', '%s')""" % \
            (title, description, request_type, 'pending',
             'no feedback', date_created, user_id)
        self.cur.execute(create_request)
        self.conn.commit()

    def get_user_requests(self, user_id):
        """
        get all the requests of a user
        """
        self.cur.execute(
            "SELECT * FROM requests WHERE user_id = %s;", [user_id])
        self.requests = self.cur.fetchall()
        self.all_requests = []
        for request in self.requests:
            self.requests_labeled = {'request_id': request[0], 'title': request[1], 'description':  request[2],
                                     'type':  request[3], 'status':  request[4], 'date_created':  request[5]}
            self.all_requests.append(self.requests_labeled)

    def get_specific_request(self, user_id, requestId):
        """
        retrieve specific request from the database
        """
        self.cur.execute(
            "SELECT * FROM requests WHERE user_id = %s and id = %s ;", (user_id, requestId))
        self.request = self.cur.fetchone()
        self.request_labeled = {'request_id': self.request[0], 'title': self.request[1], 'description': self.request[2],
                                'type': self.request[3], 'status': self.request[4], 'date_created': self.request[5]}

    def update_request(self, title, description, request_type, requestId, date):
        self.cur.execute("UPDATE requests SET title=%s, description=%s, request_type=%s , status=%s , date_created=%s WHERE id=%s;",
                         (title, description, request_type, 'pending', date, requestId))
        self.conn.commit()

    def all_users_requests(self):
        self.cur.execute("SELECT * FROM requests")
        self.requests = self.cur.fetchall()
        self.every_request = []
        for request in self.requests:
            self.requests_labeled = {'request_id': request[0], 'title': request[1], 'description':  request[2], 'type':  request[3],
                                     'status':  request[4], 'feedback': request[5], 'date_created':  request[6], 'user_id': request[7]}
            self.every_request.append(self.requests_labeled)

    def request_status(self, request_id):
        """
        query the status of a request
        """
        self.cur.execute(
            "SELECT * FROM requests WHERE id = %s ;", (request_id,))
        self.requests = self.cur.fetchone()

    def update_request_status(self, status, request_id):
        """
        change the status of a request
        """
        self.cur.execute(
            "UPDATE requests SET status=%s WHERE id=%s;", (status, request_id))
        self.conn.commit()
