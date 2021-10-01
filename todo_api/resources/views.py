from flask_restful import Resource

from ..extensions import auth


class AuthView(Resource):
    @auth.login_required
    def post(self):
        return "", 200
