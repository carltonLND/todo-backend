"""Factory for initalizing app"""
from flask import Flask

from .config import DEBUG, HOST, PORT
from .extensions import cors, db
from .resources import (
    icons_api,
    task_group_api,
    tasks_api,
    users_api,
    views_api,
)


def initialize_app():
    """Initialises the app with imported extentions"""
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    register_all_extensions(app)
    register_all_blueprints(app)
    return app


def register_all_extensions(app):
    """Registers flask extensions"""
    db.init_app(app)
    cors.init_app(app)


def register_all_blueprints(app):
    """Registers flask blueprints from resources import"""
    app.register_blueprint(views_api(), url_prefix="/v1")
    app.register_blueprint(users_api(), url_prefix="/v1")
    app.register_blueprint(tasks_api(), url_prefix="/v1")
    app.register_blueprint(icons_api(), url_prefix="/v1")
    app.register_blueprint(task_group_api(), url_prefix="/v1")


def run():
    app = initialize_app()
    with app.app_context():
        db.create_all()
    app.run(debug=DEBUG, host=HOST, port=PORT)
