# HomeMate/server/run.py

from app.config import DevelopmentConfig
from app import app_creator
from dotenv import load_dotenv
import os


load_dotenv()
host = os.getenv('BACKEND_HOST')

HomeMate, celery = app_creator(DevelopmentConfig)
if __name__ == '__main__':
    HomeMate.run(host=host, debug=True, port=6969)