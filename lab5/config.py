import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'impossible_to_guess'
    
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"