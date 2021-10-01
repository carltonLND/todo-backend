from os import environ
from secrets import token_urlsafe

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

SQLALCHEMY_DATABASE_URI = environ.get("db_uri")
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = token_urlsafe(24)

DEBUG = environ.get("app_debug")
HOST = environ.get("app_host")
PORT = environ.get("app_port")
