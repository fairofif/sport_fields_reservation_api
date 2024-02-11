from appflask import app
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
        data = {"data": "Hello"}
        return (jsonify(data))


    @app.route('/test')
    def test():
        data = {"data": "Hello"}
        return (jsonify(data))

    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        username = data['username']
        password = data['password']
        query = "select * from Player where username = '"+username+"' and password = '"+password+"'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        if cursor.rowcount != 0:
            msg = {"message": "Login Success"}
        else:
            msg = {"message": "Login Failed"}
        cursor.close()
        conn.close()
        return jsonify(msg)