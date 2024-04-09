import pymysql
from flask import (
    jsonify,
    request
)
from db_config import mysql
from dotenv import load_dotenv
from datetime import datetime
import calendar

def admin_booking_configure_routes(app):
    ## static
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

    def findUsernameFromToken(token):
        query = f"SELECT Admin_username FROM Admin_Login_Token WHERE token = '{token}'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data['Admin_username']

    def calculateHourFrom2Times(start_time_str, end_time_str):
        # Parse time strings to datetime objects
        start_time = datetime.strptime(start_time_str, "%H:%M:%S")
        end_time = datetime.strptime(end_time_str, "%H:%M:%S")

        # Calculate the time difference
        time_difference = end_time - start_time

        # Round up to the nearest hour
        hours = (time_difference.total_seconds() + 3600 - 1) // 3600

        return int(hours)


    @app.route('/admin/reservation/<booking_status>', methods=['GET'])
    def admin_get_booking_by_status(booking_status):
        token = request.headers['token']
        if checkAdminToken(token):
            username = findUsernameFromToken(token)
            query = (
                "SELECT Sport_Field.Admin_username, Sport_Field.id venue_id, Sport_Field.name venue_name, "
                + "Sport_Field.price_per_hour, Sport_Kind.id sport_kind_id, Fields.id field_id, Fields.number field_number, "
                + "Sport_Kind.name sport_kind_name, Reservation.id reservation_id, Reservation.Player_username host_name, Reservation.name mabar_name, "
                + "Reservation.date playing_date, Reservation.time_start, Reservation.time_end, Reservation.booking_status, "
                + "Reservation.payment_credential_url FROM Sport_Field "
                + "INNER JOIN Fields ON (Sport_Field.id = Fields.Sport_Field_id) "
                + "INNER JOIN Sport_Kind ON (Sport_Field.Sport_Kind_id = Sport_Kind.id) "
                + "INNER JOIN Reservation ON (Fields.id = Reservation.Field_id) "
                + f"WHERE Sport_Field.Admin_username = '{username}' AND Reservation.booking_status = '{booking_status}'"
            )
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            results = cursor.fetchall()
            rows = cursor.rowcount
            cursor.close()
            conn.close()

            data = []
            for i in range(rows):
                item = {
                    'reservation_id': results[i]['reservation_id'],
                    'host_name': results[i]['host_name'],
                    'mabar_name': results[i]['mabar_name'],
                    'playing_date': str(results[i]['playing_date']),
                    'time_start': str(results[i]['time_start']),
                    'time_end': str(results[i]['time_end']),
                    'venue_id': results[i]['venue_id'],
                    'venue_name': results[i]['venue_name'],
                    'total_price': int(results[i]['price_per_hour']) * calculateHourFrom2Times(str(results[i]['time_start']), str(results[i]['time_end'])),
                    'sport_kind_id': results[i]['sport_kind_id'],
                    'sport_kind_name': results[i]['sport_kind_name'],
                    'field_id': results[i]['field_id'],
                    'field_number': results[i]['field_number'],
                }
                data = data + [item]
            response = {
                'get_status': True,
                'message': 'Retrieve reservation successfully',
                'data': data
            }
            code = 200
        else:
            response = {
                'get_status': False,
                'message': 'Token is expired',
                'data': None
            }
            code = 401
        return jsonify(response), code