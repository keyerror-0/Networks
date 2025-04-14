import os 

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret0keey'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
    'postgresql+psycopg2://postgres:postgres@localhost:5432/postgres-local'