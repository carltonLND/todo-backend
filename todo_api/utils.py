"""Additional functions and classes used by app"""
from argon2.exceptions import VerifyMismatchError
from flask import abort, g, jsonify
from flask_restful import fields

from . import models
from .extensions import auth


class CustomDate(fields.Raw):
    """class for marshalling datetimes"""

    def format(self, value):
        return value.strftime("%a, %d %b %Y")


class CustomCount(fields.Raw):
    """class for marhsalling object count"""

    def format(self, value):
        return len(value)


@auth.verify_token
def verify_token(token):
    user = models.User.verify_auth_token(token)
    if user:
        g.user = user
        return True
    return False


def verify_login(email, password):
    user = models.User.verify_email(email)
    try:
        user.verify_password(password)
    except (VerifyMismatchError, AttributeError):
        return False
    else:
        g.user = user
        return True


def json_abort(status, message=None):
    """Abort function that returns JSON instead of HTML"""
    data = {"abort": {"message": message, "status": status}}
    response = jsonify(data)
    response.status_code = status
    abort(response)


def get_icon(id):
    """Attempts to retrieve task by id"""
    icon = models.Icon.query.get(id)
    if not icon:
        json_abort(404, "Icon does not exist")
    return icon


def get_task(id):
    """Attempts to retrieve task by id, then checks owner_id foreign key"""
    task = models.Task.query.get(id)
    if not task:
        json_abort(404, "Task does not exist")
    elif not task.owner_id == g.user.id:
        json_abort(403, "Forbidden")
    else:
        return task


def get_task_group(id):
    """Attempts to retrieve task group by id, then checks owner_id foreign key"""
    task_group = models.TaskGroup.query.get(id)
    if not task_group:
        json_abort(404, "Task group does not exists")
    elif not task_group.owner_id == g.user.id:
        json_abort(401, "Unauthorized Access")
    else:
        return task_group


def admin_only(func):
    """Decorator to enforce admin restrictions on resources"""

    def check_admin(*args, **kwargs):
        if g.user.is_admin:
            return func(*args, **kwargs)
        json_abort(401, message="Unauthorized Access: Not Admin")

    return check_admin


user_fields = {
    "email": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
}

icon_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "svg": fields.String,
}

task_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String,
    "due_date": CustomDate,
    "created_at": CustomDate,
    "is_completed": fields.Boolean,
}


task_group_list_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "is_fav": fields.Boolean,
    "icon_id": fields.Integer,
    "tasks": CustomCount,
}

task_group_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "is_fav": fields.Boolean,
    "icon_id": fields.Integer,
    "tasks": fields.Nested(task_fields),
}
