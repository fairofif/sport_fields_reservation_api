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
    # ============================= ROUTES ==================================== #

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

    @app.route('/player/auth/login', methods=['POST'])
    def player_login():
        data = request.json
        username = data['username']
        password = data['password']
        query = "SELECT username FROM Player WHERE username = '"+username+"'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        if cursor.rowcount == 0:
            ## if username doesn't exists
            response = {
                "login_status": False,
                "message": "Username not found",
                "token": "NULL",
                "username": "NULL",
                "name": "NULL",
                "ava_url": "NULL"
            }
            cursor.close()
            conn.close()
        else:
            ## username exist
            query = "SELECT * FROM Player WHERE username = '"+username+"' AND password = '"+password+"'"
            cursor.execute(query)
            if cursor.rowcount == 0:
                ## password not valid
                response = {
                    "login_status": False,
                    "message": "Password doesn't match",
                    "token": "NULL",
                    "username": "NULL",
                    "name": "NULL",
                    "ava_url": "NULL"
                }
                cursor.close()
                conn.close()
            else:
                ## login valid
                token = newPlayerToken()

                ## delete existing token within username
                query = "DELETE FROM Player_Login_Token WHERE Player_username='"+username+"'"
                cursor.execute(query)
                conn.commit()

                query = "INSERT INTO Player_Login_Token VALUES ('"+token+"', '"+username+"', CURRENT_TIMESTAMP())"

                cursor.execute(query)
                conn.commit()

                query = "SELECT * FROM Player WHERE username = '"+username+"'"
                cursor.execute(query)
                read_row = cursor.fetchone()
                cursor.close()
                conn.close()

                response = {
                    "login_status": True,
                    "message": "Login Successfully",
                    "token": token,
                    "username": username,
                    "name": read_row['name'],
                    "ava_url": read_row['ava_url']
                }
        return response

    @app.route('/player/auth/relogin', methods=['GET'])
    def player_relogin():
        header = request.headers
        token = header['token']
        query = "SELECT token FROM Player_Login_Token WHERE token = '"+token+"'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        if cursor.rowcount == 0:
            response = {
                "relogin_status": False,
                "username": "NULL",
                "name": "NULL",
                "ava_url": "NULL",
                "message": "Token is already expired"
            }
        else:
            query = ("SELECT Player.username, Player.name, Player.ava_url, Player_Login_Token.token FROM Player"
                     + " INNER JOIN Player_Login_Token ON"
                     + " (Player_Login_Token.Player_username = Player.username)"
                     + " WHERE Player_Login_Token.token = '"+token+"'")
            cursor.execute(query)
            read_row = cursor.fetchone()
            response = {
                "relogin_status": True,
                "username": read_row['username'],
                "name": read_row['name'],
                "ava_url": read_row['ava_url'],
                "message": "Token is valid, relogin successfully"
            }
        cursor.close()
        conn.close()

        return response
