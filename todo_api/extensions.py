from argon2 import PasswordHasher
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

# api instances
api = Api()

# database instances
db = SQLAlchemy()

# cors instances
cors = CORS()

# auth instances
HASHER = PasswordHasher()
auth = HTTPTokenAuth()
