# HomeMate/server/app/config.py

import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()
class DevelopmentConfig:
    FRONTEND_URL = os.getenv('FRONTEND_URL')
    BACKEND_URL = os.getenv('BACKEND_URL')
    SERVER_NAME = os.getenv('SERVER_NAME')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # JWT 
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=3600)
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_SAMESITE = 'Strict'
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_COOKIE_DOMAIN = f".{os.getenv('DOMAIN_NAME')}"
    JWT_CSRF_IN_COOKIES = True
    # Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587 #465
    MAIL_NAME = os.getenv('MAIL_NAME')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = True #SSL
    # Celery
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
    # Caching
    CACHE_TYPE='RedisCache'
    CACHE_REDIS_HOST='localhost'
    CACHE_REDIS_PORT=6379
    CACHE_REDIS_DB=0
    CACHE_REDIS_URL = os.getenv('CACHE_REDIS_URL')
