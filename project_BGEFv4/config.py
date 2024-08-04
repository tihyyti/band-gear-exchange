import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://uuuuuuuu:xxxxxxxx@localhost/db_BGEFv4')
    SQLALCHEMY_TRACK_MODIFICATIONS = False