# /migtation.py

# create the tables for the application
import psycopg2
from project.config import conn


def migration():
    cur = conn.cursor()

    try:
        # delete tables if they exist
        cur.execute("DROP TABLE IF EXISTS users,requests;")


        # create user table
        users = """CREATE TABLE users(
                                    id SERIAL PRIMARY KEY,
                                    firstname VARCHAR(50),
                                    lastname  VARCHAR(50),
                                    email VARCHAR(50) UNIQUE,
                                    password VARCHAR(50),
                                    role INT

                            );"""
        # create requests table
        requests = """CREATE TABLE requests(
                                    id SERIAL PRIMARY KEY,
                                    title VARCHAR(50),
                                    description TEXT,
                                    trackertype VARCHAR(50),
                                    status VARCHAR(50),
                                    feedback VARCHAR(50),
                                    datecreated TIMESTAMP,
                                    userid INT references users(id)
                            );"""
        cur.execute(users)
        cur.execute(requests)
        create_user_admin = """INSERT INTO
                users  (email, firstname, lastname, password, role)
                VALUES ('%s','%s','%s','%s', %d)""" % ('admin@gmail.com','jane', 'joseph','12345', 1)
        cur.execute(create_user_admin)
        conn.commit()

    except Exception as e:
        print('error',e)


migration()
