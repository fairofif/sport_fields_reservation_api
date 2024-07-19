import pymysql
from flask import (
    jsonify,
    request
)
from db_config import mysql
from dotenv import load_dotenv
import datetime
load_dotenv(override=True)
import os


def profile_configure_routes(app):
     # ==== SETUP ===== #
    UPLOAD_FOLDER_ADMIN = os.getenv("UPLOAD_FOLDER_ADMIN")
    UPLOAD_FOLDER_PLAYER = os.getenv("UPLOAD_FOLDER_PLAYER")
    app.config['UPLOAD_FOLDER_ADMIN'] = UPLOAD_FOLDER_ADMIN
    app.config['UPLOAD_FOLDER_PLAYER'] = UPLOAD_FOLDER_PLAYER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = set(['heic', 'jpg', 'jpeg', 'png', 'gif'])
    BASE_URL_IMAGE = os.getenv("BASE_URL_IMAGE")

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # ROUTE

    @app.route('/user-info', methods=['PUT'])
    def editUserInformation():
        token = request.headers['token']
        if checkPlayerToken(token) or checkAdminToken(token):
            username_session, role = getUsernameFromToken(token)
            data = request.json
            columns = [
                'username',
                'name',
                'phone'
            ]
            if role == 'admin':
                query = "UPDATE Admin SET "
            else:
                query = "UPDATE Player SET "
            for i in range(len(columns)):
                if data[columns[i]] != None:
                    query = query + columns[i] + " = '" + str(data[columns[i]]) + "', "
            query = query + "last_edited = CURRENT_TIMESTAMP() "
            query = query + f"WHERE username = '{username_session}'"

            if data['username'] != None:
                if usernameIsExistsInAdmin(data['username']) or usernameIsExistsInPlayer(data['username']):
                    response = {
                        'status': False,
                        'message': f"username {data['username']} is exists",
                        'data': None
                    }
                    code = 409
                else:
                    conn = mysql.connect()
                    cursor = conn.cursor(pymysql.cursors.DictCursor)
                    cursor.execute(query)
                    conn.commit()
                    if role == 'admin':
                        query = f"SELECT * FROM Admin WHERE username = '{data['username']}'"
                        cursor.execute(query)
                        result = cursor.fetchone()
                        response = {
                            'status': True,
                            'message': "Edit profile success",
                            'data': {
                                'username': result['username'],
                                'name': result['name'],
                                'phone': result['phone'],
                                'ava_url': result['ava_url'],
                                'role': 'admin'
                            }
                        }
                        code = 200
                    else:
                        query = f"SELECT * FROM Player WHERE username = '{data['username']}'"
                        cursor.execute(query)
                        result = cursor.fetchone()
                        response = {
                            'status': True,
                            'message': "Edit profile success",
                            'data': {
                                'username': result['username'],
                                'name': result['name'],
                                'phone': result['phone'],
                                'ava_url': result['ava_url'],
                                'role': 'player'
                            }
                        }
                        code = 200
                    cursor.close()
                    conn.close()
            else:
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute(query)
                conn.commit()
                if role == 'admin':
                    query = f"SELECT * FROM Admin WHERE username = '{username_session}'"
                    cursor.execute(query)
                    result = cursor.fetchone()
                    response = {
                        'status': True,
                        'message': "Edit profile success",
                        'data': {
                            'username': result['username'],
                            'name': result['name'],
                            'phone': result['phone'],
                            'ava_url': result['ava_url'],
                            'role': 'admin'
                        }
                    }
                    code = 200
                else:
                    query = f"SELECT * FROM Player WHERE username = '{username_session}'"
                    cursor.execute(query)
                    result = cursor.fetchone()
                    response = {
                        'status': True,
                        'message': "Edit profile success",
                        'data': {
                            'username': result['username'],
                            'name': result['name'],
                            'phone': result['phone'],
                            'ava_url': result['ava_url'],
                            'role': 'player'
                        }
                    }
                    code = 200
                cursor.close()
                conn.close()
        else:
            response = {
                'status': False,
                'message': "Token is expired",
                'data': None
            }
            code = 401
        return jsonify(response), code


    @app.route('/user-info/ava', methods=['POST'])
    def upload_ava_profile():
        token = request.headers['token']
        if checkAdminToken(token) or checkPlayerToken(token):
            username, role = getUsernameFromToken(token)
            if 'file' not in request.files:
                response = {
                    'status': False,
                    'message': 'No file part in request',
                    'data': None
                }
                code = 400
            else:
                file_ = request.files['file']
                if not file_ or file_.filename == '':
                    response = {
                        'status': False,
                        'message': 'No selected file',
                        'data': None
                    }
                    code = 400
                else:
                    if file_ and allowed_file(file_.filename):
                        file_extension = file_.filename.rsplit('.', 1)[1].lower()
                        if role == 'admin':
                            custom_filename = f"admin_{username}_{get_current_time_string()}."
                        else:
                            custom_filename = f"player_{username}_{get_current_time_string()}."
                        filename = custom_filename + file_extension
                        if role == 'admin':
                            file_.save(os.path.join(app.config['UPLOAD_FOLDER_ADMIN'], filename))
                            url_image = f"{BASE_URL_IMAGE}/admin_profile/{filename}"
                            query = f"UPDATE Admin SET ava_url = '{url_image}' WHERE username = '{username}'"
                        else:
                            file_.save(os.path.join(app.config['UPLOAD_FOLDER_PLAYER'], filename))
                            url_image = f"{BASE_URL_IMAGE}/player_profile/{filename}"
                            query = f"UPDATE Player SET ava_url = '{url_image}' WHERE username = '{username}'"
                        conn = mysql.connect()
                        cursor = conn.cursor(pymysql.cursors.DictCursor)
                        cursor.execute(query)
                        conn.commit()
                        cursor.close()
                        conn.close()

                        if role == 'admin':
                            query = f"SELECT * FROM Admin WHERE username = '{username}'"
                        else:
                            query = f"SELECT * FROM Player WHERE username = '{username}'"
                        conn = mysql.connect()
                        cursor = conn.cursor(pymysql.cursors.DictCursor)
                        cursor.execute(query)
                        result = cursor.fetchone()
                        cursor.close()
                        conn.close()

                        response = {
                            'status': True,
                            'message': 'Change ava success',
                            'data': {
                                'username': result['username'],
                                'ava_url': result['ava_url'],
                                'phone': result['phone'],
                                'name': result['name'],
                                'role': role
                            }
                        }
                        code = 200
                    else:
                        response = {
                            'status': False,
                            'message': 'Extension of the file is not allowed',
                            'data': None
                        }
                        code = 400
        else:
            response = {
                'status': False,
                'message': 'Token is expired',
                'data': None
            }
            code = 401

        return jsonify(response), code

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

def getUsernameFromToken(token):
    query = f"SELECT token, Admin_username username FROM Admin_Login_Token WHERE token = '{token}'"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    if cursor.rowcount != 0:
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result['username'], 'admin'
    else:
        query = f"SELECT token, Player_username username FROM Player_Login_Token WHERE token = '{token}'"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result['username'], 'player'

def get_current_time_string():
        current_time = datetime.datetime.now().time()
        formatted_time = current_time.strftime('%H%M%S%f')[:-3]  # Exclude microseconds
        return formatted_time