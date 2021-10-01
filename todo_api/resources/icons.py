from flask import g
from flask_restful import Resource, marshal, reqparse

from .. import models
from ..extensions import auth
from ..utils import admin_only, get_icon, icon_fields, json_abort


class IconList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "name",
            required=True,
            help="No icon name provided",
            location=["form", "json"],
        )
        self.reqparse.add_argument(
            "svg",
            required=True,
            help="No icon svg text provided.",
            location=["json"],
        )
        super().__init__()

    def get(self):
        icon_list = models.Icon.query.all()
        if not icon_list:
            json_abort(204)
        response = {
            "message": "Retrieved all icons",
            "icons": marshal(icon_list, icon_fields),
        }
        return response, 200

    @auth.login_required
    @admin_only
    def post(self):
        kwargs = self.reqparse.parse_args()
        models.Icon.create_icon(**kwargs)
        response = {"message": "Icon created"}
        return response, 201


class Icon(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "name",
            help="No icon name provided",
            location=["form", "json"],
        )
        self.reqparse.add_argument(
            "svg",
            help="No icon svg text provided.",
            location=["json"],
        )
        super().__init__()

    def get(self, id):
        icon = get_icon(id)
        response = {
            "message": "Retrieved icon",
            "icon": marshal(icon, icon_fields),
        }
        return response, 200

    @auth.login_required
    @admin_only
    def put(self, id):
        icon = get_icon(id)
        kwargs = self.reqparse.parse_args()
        icon.edit_icon(**kwargs)
        return {"message": "Icon updated"}

    @auth.login_required
    @admin_only
    def delete(self, id):
        icon = get_icon(id)
        icon.delete_icon()
        return {"message": "Icon deleted"}, 200
