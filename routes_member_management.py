import pymysql
from flask import (
    jsonify,
    request
)
from db_config import mysql



def member_management_configure_routes(app):
    # STATIC
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

    def isReservationOpenMember(reservation_id):
        query = f"SELECT is_open_member from Reservation WHERE id = '{reservation_id}'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result['is_open_member'] == 1:
            return True
        else:
            return False

    def findUsernameFromToken(token):
        query = f"SELECT Player_username FROM Player_Login_Token WHERE token = '{token}'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data['Player_username']

    def isPlayerNotAHost(reservation_id, username):
        query = f"SELECT id, Player_username FROM Reservation WHERE id = '{reservation_id}' AND Player_username = '{username}'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        rowcount = cursor.rowcount
        cursor.close()
        conn.close()

        if rowcount != 0:
            return False
        else:
            return True

    def isPlayerNotAlreadyInAReservationAsMember(reservation_id, username):
        query = f"SELECT Reservation_id, Player_username FROM Reservation_Member WHERE Reservation_id = '{reservation_id}' AND Player_username = '{username}'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        rowcount = cursor.rowcount
        cursor.close()
        conn.close()

        if rowcount != 0:
            return False
        else:
            return True

    def isPlayerExists(username):
        query = f"SELECT username FROM Player WHERE username = '{username}'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        rowcount = cursor.rowcount
        cursor.close()
        conn.close()

        if rowcount != 0:
            return True
        else:
            return False

    def isReservationExists(reservation_id):
        query = f"SELECT id FROM Reservation WHERE id = '{reservation_id}'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        rowcount = cursor.rowcount
        cursor.close()
        conn.close()

        if rowcount != 0:
            return True
        else:
            return False

    # ROUTES
    @app.route('/player/reservation/invite/<reservation_id>/<invited_username>', methods=['POST'])
    def invite_player_to_reservation(reservation_id, invited_username):
        token = request.headers['token']
        if checkPlayerToken(token):
            username = findUsernameFromToken(token)
            if not isPlayerNotAHost(reservation_id, username):
                if isPlayerExists(invited_username):
                    if isPlayerNotAHost(reservation_id, invited_username):
                        if isPlayerNotAlreadyInAReservationAsMember(reservation_id, invited_username):
                            query = f"INSERT INTO Reservation_Member VALUES ('{reservation_id}', '{invited_username}')"
                            conn = mysql.connect()
                            cursor = conn.cursor(pymysql.cursors.DictCursor)
                            cursor.execute(query)
                            conn.commit()
                            cursor.close()
                            conn.close()

                            response = {
                                'invite_status': True,
                                'message': f"{invited_username} now is member of reservation {reservation_id}",
                                'data': {
                                    'reservation_id': reservation_id
                                }
                            }
                            code = 200
                        else:
                            response = {
                                'invite_status': False,
                                'message': f"{invited_username} is already in reservation {reservation_id} before",
                                'data': None
                            }
                            code = 409
                    else:
                        response = {
                            'invite_status': False,
                            'message': f"This user is already a host of reservation {reservation_id}",
                            'data': None
                        }
                        code = 403
                else:
                    response = {
                        'invite_status': False,
                        'message': f"{invited_username} not found as a player in database",
                        'data': None
                    }
                    code = 404
            else:
                response = {
                    'invite_status': False,
                    'message': f"{invited_username} failed to be invited, {username} not a host of reservation {reservation_id}",
                    'data': None
                }
                code = 403
        else:
            response = {
                'invite_status': False,
                'message': 'Token is expired',
                'data': None
            }
            code = 401

        return jsonify(response), code

    @app.route('/player/reservation/join/<reservation_id>', methods=['POST'])
    def join_a_reservation(reservation_id):
        token = request.headers['token']
        if checkPlayerToken(token):
            username = findUsernameFromToken(token)
            if isReservationOpenMember(reservation_id):
                if isPlayerNotAHost(reservation_id, username):
                    if isPlayerNotAlreadyInAReservationAsMember(reservation_id, username):
                        query = f"INSERT INTO Reservation_Member VALUES ('{reservation_id}', '{username}')"
                        conn = mysql.connect()
                        cursor = conn.cursor(pymysql.cursors.DictCursor)
                        cursor.execute(query)
                        conn.commit()
                        cursor.close()
                        conn.close()

                        response = {
                            'join_status': True,
                            'message': f"{username} now is member of reservation {reservation_id}",
                            'data': {
                                'reservation_id': reservation_id
                            }
                        }
                        code = 200

                    else:
                        response = {
                            'join_status': False,
                            'message': f"This user is already a member of this reservation {reservation_id}",
                            'data': None
                        }
                        code = 409
                else:
                    response = {
                        'join_status': False,
                        'message': f"You are already a host of this reservation {reservation_id}",
                        'data': None
                    }
                    code = 403
            else:
                response = {
                    'join_status': False,
                    'message': f"Reservation {reservation_id} is not open member",
                    'data': None
                }
                code = 403
        else:
            response = {
                'join_status': False,
                'message': 'Token is expired',
                'data': None
            }
            code = 401

        return jsonify(response), code

    @app.route('/player/reservation/members/<reservation_id>', methods=['GET'])
    def get_list_members_of_reservation(reservation_id):
        token = request.headers['token']
        if checkPlayerToken(token):
            if isReservationExists(reservation_id):
                members = []
                query = f"SELECT Player_username FROM Reservation WHERE id = '{reservation_id}'"
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute(query)
                result = cursor.fetchone()
                cursor.close()
                conn.close()
                item = {
                    'username': result['Player_username'],
                    'role': 'host'
                }
                members = members + [item]
                query = f"SELECT Player_username FROM Reservation_Member WHERE Reservation_id = '{reservation_id}'"
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute(query)
                result = cursor.fetchall()
                rowcount = cursor.rowcount
                cursor.close()
                conn.close()
                for i in range(rowcount):
                    item = {
                        'username': result[i]['Player_username'],
                        'role': 'member'
                    }
                    members = members + [item]
                response = {
                    'get_status': True,
                    'message': f"List member of reservation {reservation_id} successfully retrieved",
                    'data': members
                }
                code = 200
            else:
                response = {
                    'get_status': False,
                    'message': f"Reservation {reservation_id} is not exists",
                    'data': None
                }
                code = 404
        else:
            response = {
                'get_status': False,
                'message': 'Token is expired',
                'data': None
            }
            code = 401
        return jsonify(response), code

    @app.route('/player/reservation/kick/<reservation_id>/<username>', methods=['DELETE'])
    def kick_a_member_from_reservation(reservation_id, username):
        token = request.headers['token']
        if checkPlayerToken(token):
            username_requester = findUsernameFromToken(token)
            if isReservationExists(reservation_id):
                if not isPlayerNotAHost(reservation_id, username_requester):
                    if isPlayerNotAHost(reservation_id, username):
                        if not isPlayerNotAlreadyInAReservationAsMember(reservation_id, username):
                            query = f"DELETE FROM Reservation_Member WHERE Reservation_id = '{reservation_id}' AND Player_username = '{username}'"
                            conn = mysql.connect()
                            cursor = conn.cursor(pymysql.cursors.DictCursor)
                            cursor.execute(query)
                            conn.commit()
                            cursor.close()
                            conn.close()

                            response = {
                                'kick_status': True,
                                'message': f"{username} has been removed from reservation {reservation_id}",
                                'data': {
                                    'reservation_id': reservation_id
                                }
                            }
                            code = 200
                        else:
                            response = {
                                'kick_status': False,
                                'message': f"{username} is not a member of reservation {reservation_id}",
                                'data': None
                            }
                            code = 404
                    else:
                        response = {
                            'kick_status': False,
                            'message': f"Can't kick a host",
                            'data': None
                        }
                        code = 403
                else:
                    response = {
                        'kick_status': False,
                        'message': f"Only host could kick a member, {username_requester} is not a host of reservation {reservation_id}",
                        'data': None
                    }
                    code = 403
            else:
                response = {
                    'kick_status': False,
                    'message': f"Reservation {reservation_id} is not exists",
                    'data': None
                }
                code = 404
        else:
            response = {
                'get_status': False,
                'message': 'Token is expired',
                'data': None
            }
            code = 401
        return jsonify(response), code
