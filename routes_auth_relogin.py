import pymysql
from flask import (
    jsonify,
    request
)
from db_config import mysql
from token_generator import newUserToken
from dotenv import load_dotenv
load_dotenv()
import os

def relogin_configure_routes(app):
    @app.route('/auth/relogin', methods=['GET'])
    def auth_relogin():
        header = request.headers
        token = header['token']
        query = "SELECT token FROM Player_Login_Token WHERE token = '"+token+"'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        if cursor.rowcount == 0:
            query = "SELECT token FROM Admin_Login_Token WHERE token = '"+token+"'"
            cursor.execute(query)
            if cursor.rowcount == 0:
                response = {
                    "relogin_status": False,
                    "message": "Token is already expired",
                    "data": {
                        "username": None,
                        "name": None,
                        "ava_url": None,
                        "phone": None,
                        "role": None
                    }
                }
            else:
                query = ("SELECT Admin.username, Admin.name, Admin.ava_url, Admin.phone, Admin_Login_Token.token FROM Admin"
                     + " INNER JOIN Admin_Login_Token ON"
                     + " (Admin_Login_Token.Admin_username = Admin.username)"
                     + " WHERE Admin_Login_Token.token = '"+token+"'")
                cursor.execute(query)
                read_row = cursor.fetchone()
                response = {
                    "relogin_status": True,
                    "message": "Token is valid, relogin successfully",
                    "data": {
                        "username": read_row['username'],
                        "name": read_row['name'],
                        "ava_url": read_row['ava_url'],
                        "phone": read_row['phone'],
                        "role": "admin"
                    }
                }
        else:
            query = ("SELECT Player.username, Player.name, Player.ava_url, Player.phone, Player_Login_Token.token FROM Player"
                     + " INNER JOIN Player_Login_Token ON"
                     + " (Player_Login_Token.Player_username = Player.username)"
                     + " WHERE Player_Login_Token.token = '"+token+"'")
            cursor.execute(query)
            read_row = cursor.fetchone()
            response = {
                "relogin_status": True,
                "message": "Token is valid, relogin successfully",
                "data": {
                    "username": read_row['username'],
                    "name": read_row['name'],
                    "ava_url": read_row['ava_url'],
                    "phone": read_row['phone'],
                    "role": "player"
                }
            }
        cursor.close()
        conn.close()

        return jsonify(response)