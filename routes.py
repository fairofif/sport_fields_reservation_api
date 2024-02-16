from app import app
import pymysql
from flask import (
    jsonify,
    request
)
from db_config import mysql
from flask_swagger_ui import get_swaggerui_blueprint


def configure_routes(app):
    SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
    API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "Test application"
    },
    )

    app.register_blueprint(swaggerui_blueprint)

    @app.route('/')
    def greet():
        data = {"data": "Hello Developer, go to http://rofif.my.id/api/docs for documentations"}
        return (jsonify(data))
