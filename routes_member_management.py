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


    # ROUTES

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