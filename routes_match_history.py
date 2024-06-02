import pymysql
from flask import (
    jsonify,
    request
)
from db_config import mysql
from static import newMatchHistoryUUID

def match_history_configure_routes(app):
    # static
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

    def usernameIsAHost(username, reservation_id):
        query = f"SELECT * FROM Reservation WHERE Player_username = '{username}' AND id = '{reservation_id}'"
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

    def findBookingStatusOfReservation(reservation_id):
        query = f"SELECT booking_status FROM Reservation WHERE id = '{reservation_id}'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        return result['booking_status']

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

    def reservationStatus(reservation_id):
        query = f"SELECT booking_status FROM Reservation WHERE id = '{reservation_id}'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        return result['booking_status']


    # ROUTES

    @app.route('/player/reservation/match-history', methods=['GET'])
    def get_match_history():
        token = request.headers['token']
        reservation_id = request.json['reservation_id']
        if checkPlayerToken(token):
            username = findUsernameFromToken(token)
            query = f"SELECT * FROM Match_History WHERE Reservation_id = '{reservation_id}'"
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            results = cursor.fetchall()
            rows = cursor.rowcount
            cursor.close()
            conn.close()

            datas = []
            for i in range(rows):
                item = {
                    'match_id': results[i]['id'],
                    'reservation_id': results[i]['Reservation_id'],
                    'number': results[i]['number'],
                    'score_a': results[i]['score_a'],
                    'score_b': results[i]['score_b'],
                    'is_done': results[i]['is_done'],
                    'created_at': str(results[i]['created_at'])
                }
                datas = datas + [item]

            response = {
                'status': True,
                'message': 'Retrieve match history data success',
                'data': datas
            }
            code = 200
        else:
            response = {
                'status': False,
                'message': 'Token is expired',
                'data': datas
            }
            code = 401
        return jsonify(response), code

    @app.route('/player/reservation/match-history', methods=['POST'])
    def create_new_match_history():
        token = request.headers['token']
        body = request.json
        if checkPlayerToken(token):
            username = findUsernameFromToken(token)
            if reservationStatus(body['reservation_id']) == 'approved':
                if usernameIsAHost(username, body['reservation_id']) or not isPlayerNotAlreadyInAReservationAsMember(body['reservation_id'], username):
                    match_id = newMatchHistoryUUID()
                    query = (
                        "INSERT INTO Match_History (id, Reservation_id, number, created_at, last_updated) "
                        + f"VALUES ('{match_id}', '{body['reservation_id']}', '{body['match_number']}', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP())"
                    )
                    conn = mysql.connect()
                    cursor = conn.cursor(pymysql.cursors.DictCursor)
                    cursor.execute(query)
                    conn.commit()
                    cursor.close()
                    conn.close()

                    response = {
                        'status': True,
                        'message': 'Create history match success',
                        'data': {
                            'match_history_id': match_id
                        }
                    }
                    code = 200
                else:
                    response = {
                        'status': False,
                        'message': 'Player not a member of this reservation',
                        'data': None
                    }
                    code = 403
            else:
                response = {
                    'status': False,
                    'message': f"Reservation {body['reservation_id']} is not approved",
                    'data': None
                }
                code = 403
        else:
            response = {
                'status': False,
                'message': 'Token is expired',
                'data': None
            }
            code = 401
        return jsonify(response), code