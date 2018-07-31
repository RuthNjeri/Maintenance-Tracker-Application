# /migtation.py

# create the tables for the application

from project.config import conn
from werkzeug.security import generate_password_hash


def migration():
    """
    create the tables on the database
    """
    cur = conn.cursor()

    try:
        # delete tables if they exist
        cur.execute("DROP TABLE IF EXISTS users,requests;")
        cur.execute("DROP TABLE IF EXISTS tokens;")

        # create user table
        users = """CREATE TABLE users(
                                    id SERIAL PRIMARY KEY,
                                    first_name VARCHAR(50),
                                    last_name  VARCHAR(50),
                                    email VARCHAR(50) UNIQUE,
                                    password_hash VARCHAR(100),
                                    role INT

                            );"""
        # create requests table
        requests = """CREATE TABLE requests(
                                    id SERIAL PRIMARY KEY,
                                    title VARCHAR(50),
                                    description TEXT,
                                    request_type VARCHAR(50),
                                    status VARCHAR(50),
                                    feedback VARCHAR(50),
                                    date_created TIMESTAMP,
                                    user_id INT references users(id)
                            );"""
        # create black listed tokens table
        tokens = """CREATE TABLE tokens(
                                    id SERIAL PRIMARY KEY,
                                    expired_tokens VARCHAR(150)
                            );"""
        cur.execute(users)
        cur.execute(requests)
        cur.execute(tokens)
        password_hash = generate_password_hash('12345678')
        create_user_admin = """INSERT INTO
                users  (email, first_name, last_name, password_hash, role)
                VALUES ( '%s', '%s', '%s', '%s', %d)""" \
                % ('admin@gmail.com', 'jane', 'joseph', password_hash, 1)
        cur.execute(create_user_admin)
        conn.commit()
    except Exception as e:
        print('error', e)


migration()
