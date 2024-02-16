from app import app
import pymysql
from flask import (
    jsonify,
    request
)
from db_config import mysql
from token_generator import newPlayerToken
from dotenv import load_dotenv
load_dotenv()
import os

def player_auth_configure_routes(app):
    @app.route('/player/auth/register', methods=['POST'])
    def player_register():
        """route for register new player user"""
        data = request.json
        username = data['username']
        password = data['password']
        name = data['name']
        ava_url = os.getenv("DEFAULT_AVA_PATH")
        query = 'SELECT username FROM Player WHERE username = "'+str(username)+'"'
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        if cursor.rowcount == 0:
            query_insert = "INSERT INTO Player VALUES ('"+username+"', '"+password+"', '"+name+"', '"+ava_url+"', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP())"
            cursor.execute(query_insert)
            response = {
                "message": "Register Success",
                "register_status": True
            }
        else:
            response = {
                "message": "Username is already Exists in Database",
                "register_status": False
            }
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify(response)
