import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  # Example using SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False
