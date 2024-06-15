import pymysql
from flask import (
    jsonify,
    request
)
from db_config import mysql
from dotenv import load_dotenv
load_dotenv(override=True)


def profile_configure_routes(app):

    @app.route('/user-info/<username>', methods=['GET'])
    def getPublicUserInfoByUsername(username):
        token = request.headers['token']
        if checkAdminToken(token) or checkPlayerToken(token):
            if usernameIsExistsInAdmin(username):
                query = f"SELECT * FROM Admin WHERE username = '{username}'"
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute(query)
                result = cursor.fetchone()
                cursor.close()
                conn.close()
                response = {
                    'status': True,
                    'message': 'Get user information success',
                    'data': {
                        'role': 'admin',
                        'username': result['username'],
                        'name': result['name'],
                        'ava_url': result['ava_url'],
                        'phone': result['phone']
                    }
                }
                code = 200
            elif usernameIsExistsInPlayer(username):
                query = f"SELECT * FROM Player WHERE username = '{username}'"
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute(query)
                result = cursor.fetchone()
                cursor.close()
                conn.close()
                response = {
                    'status': True,
                    'message': 'Get user information success',
                    'data': {
                        'role': 'player',
                        'username': result['username'],
                        'name': result['name'],
                        'ava_url': result['ava_url'],
                        'phone': result['phone']
                    }
                }
                code = 200
            else:
                response = {
                    'status': False,
                    'message': 'Username is not found',
                    'data': None
                }
                code = 404
        else:
            response = {
                'status': False,
                'message': 'Token is expired',
                'data': None
            }
            code = 401
        return jsonify(response), code


# === STATIC === #
def checkPlayerToken(token):
    query = "SELECT token FROM Player_Login_Token WHERE token = '"+token+"'"

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return False
    else:
        cursor.close()
        conn.close()
        return True

def checkAdminToken(token):
    query = "SELECT token FROM Admin_Login_Token WHERE token = '"+token+"'"

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return False
    else:
        cursor.close()
        conn.close()
        return True

def usernameIsExistsInPlayer(username):
    query = f"SELECT username FROM Player WHERE username = '{username}'"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return False
    else:
        cursor.close()
        conn.close()
        return True

def usernameIsExistsInAdmin(username):
    query = f"SELECT username FROM Admin WHERE username = '{username}'"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return False
    else:
        cursor.close()
        conn.close()
        return True
