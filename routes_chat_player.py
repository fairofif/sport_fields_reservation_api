import pymysql
from flask import (
    jsonify,
    request
)
from db_config import mysql
from uuid_generator import newChatMatchUUID

def chat_player_configure_routes(app):
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

    def findUsernameFromToken(token):
        query = f"SELECT Player_username FROM Player_Login_Token WHERE token = '{token}'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data['Player_username']

    def chatMatchExists(username_player, username_admin):
        query = f"SELECT id FROM Chat_Match WHERE Player_username = '{username_player}' AND Admin_username = '{username_admin}'"
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


    @app.route('/player/chatmatch', methods=['POST'])
    def player_chat_match():
        token = request.headers['token']
        body = request.json
        admin_username = body['admin_username']
        if checkPlayerToken(token):
            player_username = findUsernameFromToken(token)
            if chatMatchExists(player_username, admin_username):
                query = f"SELECT id FROM Chat_Match WHERE Player_username = '{player_username}' AND Admin_username = '{admin_username}'"
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute(query)
                result = cursor.fetchone()
                cursor.close()
                conn.close()
                response = {
                    'status': True,
                    'message': 'Match had been created before, return the old one success',
                    'data': {
                        'id_chat_match': result['id']
                    }
                }
                code = 200
            else:
                new_id = newChatMatchUUID()
                query = f"INSERT INTO Chat_Match VALUES ('{new_id}', '{admin_username}', '{player_username}')"
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute(query)
                conn.commit()
                cursor.close()
                conn.close()
                response = {
                    'status': True,
                    'message': 'Create new match success',
                    'data': {
                        'id_chat_match': new_id
                    }
                }
                code = 200
        else:
            response = {
                'status': False,
                'message': 'Token is expired',
                'data': None
            }
            code = 401
        return jsonify(response), code