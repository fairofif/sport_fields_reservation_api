from appflask import app
import pymysql
from flask import (
    jsonify,
    request
)
from db_config import mysql


def configure_routes(app):
    @app.route('/')
    def greet():
        data = {"data": "Hello"}
        return (jsonify(data))


    @app.route('/test')
    def test():
        data = {"data": "Hello"}
        return (jsonify(data))

    @app.route('/login', methods=['GET'])
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