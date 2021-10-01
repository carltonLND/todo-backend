from flask import g
from flask_restful import Resource, marshal, reqparse

from .. import models
from ..extensions import auth
from ..utils import get_task_group, task_group_fields, task_group_list_fields


class TaskGroupList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "name",
            required=True,
            help="No group title provided",
            location=["form", "json"],
        )
        self.reqparse.add_argument(
            "description",
            help="No description provided",
            location=["form", "json"],
        )
        self.reqparse.add_argument(
            "is_fav",
            help="Boolean indicating grou is favourite",
            location=["form", "json"],
        )
        self.reqparse.add_argument(
            "icon_id",
            help="Selected icon by foreign key, default is 1",
            location=["form", "json"],
        )
        super().__init__()

    @auth.login_required
    def get(self):
        task_groups = models.TaskGroup.query.filter(
            models.TaskGroup.owner_id == g.user.id
        ).all()
        if not task_groups:
            return "", 204
        response = {
            "message": "Retrieved all user task groups",
            "task_groups": marshal(task_groups, task_group_list_fields),
        }
        return response, 200

    @auth.login_required
    def post(self):
        kwargs = self.reqparse.parse_args()
        models.TaskGroup.create_task_group(**kwargs)
        response = {"message": "Task group created"}
        return response, 201


class TaskGroup(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "name",
            help="No group title provided",
            location=["form", "json"],
        )
        self.reqparse.add_argument(
            "description",
            help="No description provided",
            location=["form", "json"],
        )
        self.reqparse.add_argument(
            "is_fav",
            help="Boolean indicating grou is favourite",
            location=["form", "json"],
        )
        self.reqparse.add_argument(
            "icon_id",
            help="Selected icon by foreign key, default is 1",
            location=["form", "json"],
        )
        super().__init__()

    @auth.login_required
    def get(self, id):
        task_group = get_task_group(id)
        response = {
            "message": "Retrieved task group",
            "task groups": marshal(task_group, task_group_fields),
        }
        return response, 200

    @auth.login_required
    def put(self, id):
        task_group = get_task_group(id)
        kwargs = self.reqparse.parse_args()
        task_group.edit_task_group(**kwargs)
        return {"message": "Task group updated"}, 200

    @auth.login_required
    def delete(self, id):
        task_group = get_task_group(id)
        task_group.delete_task_group()
        return {"message": "Task group deleted"}, 200
