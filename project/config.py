# project/config.py

import os

class BaseConfig:
    '''Base configurations'''
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'weak_full_stack'
    BCRYPT_LOG_ROUNDS = 13

class DevelopmentConfig(BaseConfig):
    '''Development configuration'''
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    BCRYPT_LOG_ROUNDS = 4 

class TestingConfig(BaseConfig):
    '''Testing configuration'''
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    BCRYPT_LOG_ROUNDS = 4

class ProductionConfig(BaseConfig):
    '''prodction configration'''
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
