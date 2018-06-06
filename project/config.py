#project/config file


import os
import psycopg2

base_dir = os.path.abspath(os.path.dirname(__file__))

try:
    #connect to database
    conn = psycopg2.connect("dbname=maintenanceapp host=localhost user=postgres password=1234")
    
except:
    print("database not connected")




class Config(object):
    """Base config class"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')


class DevConfig(Config):
    """Configuration for development"""
    DEBUG = True

class TestConfig(Config):
    """Test config"""
    TESTING = True
    DEBUG = True

class StagingConfig(Config):
    """Staging configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Staging for production"""
    DEBUG = False
    TESTING = False

         



