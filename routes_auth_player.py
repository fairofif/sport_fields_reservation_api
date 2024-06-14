import pymysql
from flask import (
    jsonify,
    request
)
from db_config import mysql
from token_generator import newUserToken
from dotenv import load_dotenv
load_dotenv(override=True)
import os

# ===== STATIC ===== #
def usernameIsNotExists(username: str):
    found = 0
    query = f"SELECT username FROM Admin WHERE username = '{username}'"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    if cursor.rowcount > 0:
        found = found + 1
    query = f"SELECT username FROM Player WHERE username = '{username}'"
    cursor.execute(query)
    if cursor.rowcount > 0:
        found = found + 1
    cursor.close()
    conn.close()
    if found > 0:
        return False
    else:
        return True


def player_auth_configure_routes(app):
    # ============================= ROUTES ==================================== #

    @app.route('/player/auth/register', methods=['POST'])
    def player_register():
        """route for register new player user"""
        data = request.json
        username = data['username']
        password = data['password']
        name = data['name']
        phone = data['phone']
        ava_url = os.getenv("DEFAULT_AVA_PATH")

        if usernameIsNotExists(username):
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            query_insert = "INSERT INTO Player VALUES ('"+username+"', '"+password+"', '"+name+"', '"+ava_url+"', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), '"+phone+"')"
            cursor.execute(query_insert)
            response = {
                "message": "Register Success",
                "register_status": True
            }
            code = 200
            conn.commit()
            cursor.close()
            conn.close()
        else:
            response = {
                "message": "Username is already Exists in Database",
                "register_status": False
            }
            code = 409
        return jsonify(response), code

    @app.route('/player/auth/login', methods=['POST'])
    def player_login():
        data = request.json
        username = data['username']
        password = data['password']
        virtual_device_id = data['virtual_device_id']
        query = "SELECT username FROM Player WHERE username = '"+username+"'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        if cursor.rowcount == 0:
            ## if username doesn't exists
            response = {
                "login_status": False,
                "message": "Username not found",
                "data": {
                    "token": None,
                    "username": None,
                    "name": None,
                    "ava_url": None,
                    "phone": None
                }
            }
            code = 404
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
                    "data": {
                        "token": None,
                        "username": None,
                        "name": None,
                        "ava_url": None,
                        "phone": None
                    }
                }
                code = 400
                cursor.close()
                conn.close()
            else:
                ## login valid
                token = newUserToken()

                ## delete existing token within device ID
                query = "DELETE FROM Player_Login_Token WHERE Virtual_Device_ID_id='"+virtual_device_id+"'"
                cursor.execute(query)
                conn.commit()

                query = "INSERT INTO Player_Login_Token VALUES ('"+token+"', '"+username+"', CURRENT_TIMESTAMP(), '"+virtual_device_id+"')"

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
                    "data": {
                        "token": token,
                        "username": username,
                        "name": read_row['name'],
                        "ava_url": read_row['ava_url'],
                        "phone": read_row['phone']
                    }
                }
                code = 200
        return jsonify(response), code

    @app.route('/player/auth/logout', methods=['DELETE'])
    def player_logout():
        header = request.headers
        token = header['token']
        query = "DELETE FROM Player_Login_Token WHERE token = '"+token+"'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        response = {
            "logout_status": True,
            "message": "Logout user in this device is successfully"
        }
        code = 200

        return jsonify(response), 200
