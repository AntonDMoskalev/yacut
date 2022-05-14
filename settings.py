import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'qlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'NVLDn9Ed0DE8lgDkn7cW7jjhRgaw'