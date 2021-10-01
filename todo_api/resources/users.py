from flask import g
from flask_restful import Resource, marshal, reqparse

from .. import models
from ..extensions import auth
from ..utils import admin_only, json_abort, user_fields, verify_login


class UserSignup(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "email",
            required=True,
            help="Error: No email provided",
            location=["form", "json"],
        )
        self.reqparse.add_argument(
            "password",
            required=True,
            help="Error: No password provided",
            location=["form", "json"],
        )
        self.reqparse.add_argument(
            "first_name",
            required=True,
            help="Error: No first name provided",
            location=["form", "json"],
        )
        self.reqparse.add_argument(
            "last_name",
            required=True,
            help="Error: No last name provided",
            location=["form", "json"],
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        result = models.User.create_user(**args)
        if result == False:
            message = {"message": "Email already exists"}
            return message, 409

        verify_login(email=args.email, password=args.password)
        token = g.user.generate_auth_token()
        response = {
            "message": "User created successfully",
            "token": token.decode("ascii"),
        }
        return response, 201


class UserLogin(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "email",
            required=True,
            help="Error: no email provided",
            location=["form", "json"],
        )
        self.reqparse.add_argument(
            "password",
            required=True,
            help="Error: No password provided",
            location=["form", "json"],
        )
        super().__init__()

    def post(self):
        kwargs = self.reqparse.parse_args()
        if verify_login(**kwargs):
            token = g.user.generate_auth_token()
            response = {
                "message": "Login Successful",
                "token": token.decode("ascii"),
            }
            return response, 200
        message = {"message": "Invalid Login Credentials"}
        return message, 401


class UserList(Resource):
    @auth.login_required
    @admin_only
    def get(self):
        user_list = models.User.query.all()
        if not user_list:
            json_abort(204)
        response = {
            "message": "Retrieved all users",
            "users": marshal(user_list, user_fields),
        }
        return response, 200
