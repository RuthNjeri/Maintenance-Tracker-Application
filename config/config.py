#config/config file

import os

class Config(object):
    """Base config class"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRETE = os.getenv('SECRET')


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

app_config = {
            'development':DevConfig,
            'testing':TestConfig,
            'staging':StagingConfig,
            'production':ProductionConfig,
            }            



