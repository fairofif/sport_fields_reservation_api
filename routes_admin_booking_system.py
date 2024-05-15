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

    def hours_from_timestamp_to_now(timestamp_str):
        # Convert the timestamp string to a datetime object
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

        # Get the current time
        current_time = datetime.now()

        # Calculate the time difference
        time_difference = current_time - timestamp

        # Extract the total hours from the time difference
        hours_difference = time_difference.total_seconds() / 3600

        # Return the number of hours as an integer
        return int(hours_difference)


    @app.route('/admin/reservation/<booking_status>', methods=['GET'])
    def admin_get_booking_by_status(booking_status):
        token = request.headers['token']
        if checkAdminToken(token):
            username = findUsernameFromToken(token)
            if booking_status == 'all':
                query = (
                    "SELECT Sport_Field.Admin_username, Sport_Field.id venue_id, Sport_Field.name venue_name, "
                    + "Sport_Field.price_per_hour, Sport_Kind.id sport_kind_id, Fields.id field_id, Fields.number field_number, "
                    + "Sport_Kind.name sport_kind_name, Reservation.id reservation_id, Reservation.Player_username host_name, Reservation.name mabar_name, "
                    + "Reservation.date playing_date, Reservation.time_start, Reservation.time_end, Reservation.booking_status, "
                    + "Reservation.created_at FROM Sport_Field "
                    + "INNER JOIN Fields ON (Sport_Field.id = Fields.Sport_Field_id) "
                    + "INNER JOIN Sport_Kind ON (Sport_Field.Sport_Kind_id = Sport_Kind.id) "
                    + "INNER JOIN Reservation ON (Fields.id = Reservation.Field_id) "
                    + f"WHERE Sport_Field.Admin_username = '{username}'"
                )
            else:
                query = (
                    "SELECT Sport_Field.Admin_username, Sport_Field.id venue_id, Sport_Field.name venue_name, "
                    + "Sport_Field.price_per_hour, Sport_Kind.id sport_kind_id, Fields.id field_id, Fields.number field_number, "
                    + "Sport_Kind.name sport_kind_name, Reservation.id reservation_id, Reservation.Player_username host_name, Reservation.name mabar_name, "
                    + "Reservation.date playing_date, Reservation.time_start, Reservation.time_end, Reservation.booking_status, "
                    + "Reservation.created_at FROM Sport_Field "
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
                    'booking_status': results[i]['booking_status'],
                    'created_at': str(results[i]['created_at']),
                    'booking_creation_age_hour': hours_from_timestamp_to_now(str(results[i]['created_at']))
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

    @app.route('/admin/reservation/<venue_id>/<booking_status>', methods=['GET'])
    def admin_get_booking_by_venue_and_status(venue_id, booking_status):
        token = request.headers['token']
        if checkAdminToken(token):
            username = findUsernameFromToken(token)
            if booking_status == 'all':
                query = (
                    "SELECT Sport_Field.Admin_username, Sport_Field.id venue_id, Sport_Field.name venue_name, "
                    + "Sport_Field.price_per_hour, Sport_Kind.id sport_kind_id, Fields.id field_id, Fields.number field_number, "
                    + "Sport_Kind.name sport_kind_name, Reservation.id reservation_id, Reservation.Player_username host_name, Reservation.name mabar_name, "
                    + "Reservation.date playing_date, Reservation.time_start, Reservation.time_end, Reservation.booking_status, "
                    + "Reservation.created_at FROM Sport_Field "
                    + "INNER JOIN Fields ON (Sport_Field.id = Fields.Sport_Field_id) "
                    + "INNER JOIN Sport_Kind ON (Sport_Field.Sport_Kind_id = Sport_Kind.id) "
                    + "INNER JOIN Reservation ON (Fields.id = Reservation.Field_id) "
                    + f"WHERE Sport_Field.Admin_username = '{username}' AND Sport_Field.id = '{venue_id}'"
                )
            else:
                query = (
                    "SELECT Sport_Field.Admin_username, Sport_Field.id venue_id, Sport_Field.name venue_name, "
                    + "Sport_Field.price_per_hour, Sport_Kind.id sport_kind_id, Fields.id field_id, Fields.number field_number, "
                    + "Sport_Kind.name sport_kind_name, Reservation.id reservation_id, Reservation.Player_username host_name, Reservation.name mabar_name, "
                    + "Reservation.date playing_date, Reservation.time_start, Reservation.time_end, Reservation.booking_status, "
                    + "Reservation.created_at FROM Sport_Field "
                    + "INNER JOIN Fields ON (Sport_Field.id = Fields.Sport_Field_id) "
                    + "INNER JOIN Sport_Kind ON (Sport_Field.Sport_Kind_id = Sport_Kind.id) "
                    + "INNER JOIN Reservation ON (Fields.id = Reservation.Field_id) "
                    + f"WHERE Sport_Field.Admin_username = '{username}' AND Sport_Field.id = '{venue_id}' AND Reservation.booking_status = '{booking_status}'"
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
                    'booking_status': results[i]['booking_status'],
                    'created_at': str(results[i]['created_at']),
                    'booking_creation_age_hour': hours_from_timestamp_to_now(str(results[i]['created_at']))
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

    @app.route('/admin/reservation/detail/<reservation_id>')
    def admin_get_detailed_booking(reservation_id):
        token = request.headers['token']
        if checkAdminToken(token):
            query = (
                "SELECT Sport_Field.Admin_username, Sport_Field.id venue_id, Sport_Field.name venue_name, "
                + "Sport_Field.price_per_hour, Sport_Kind.id sport_kind_id, Fields.id field_id, Fields.number field_number, "
                + "Sport_Kind.name sport_kind_name, Reservation.id reservation_id, Reservation.Player_username host_name, Reservation.name mabar_name, "
                + "Reservation.date playing_date, Reservation.time_start, Reservation.time_end, Reservation.booking_status, "
                + "Reservation.payment_credential_url, Reservation.upload_payment_timestamp, Reservation.created_at FROM Sport_Field "
                + "INNER JOIN Fields ON (Sport_Field.id = Fields.Sport_Field_id) "
                + "INNER JOIN Sport_Kind ON (Sport_Field.Sport_Kind_id = Sport_Kind.id) "
                + "INNER JOIN Reservation ON (Fields.id = Reservation.Field_id) "
                + f"WHERE Reservation.id = '{reservation_id}'"
            )
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            results = cursor.fetchone()
            cursor.close()
            conn.close()

            data = {
                'reservation_id': results['reservation_id'],
                'host_name': results['host_name'],
                'mabar_name': results['mabar_name'],
                'playing_date': str(results['playing_date']),
                'time_start': str(results['time_start']),
                'time_end': str(results['time_end']),
                'venue_id': results['venue_id'],
                'venue_name': results['venue_name'],
                'total_price': int(results['price_per_hour']) * calculateHourFrom2Times(str(results['time_start']), str(results['time_end'])),
                'sport_kind_id': results['sport_kind_id'],
                'sport_kind_name': results['sport_kind_name'],
                'field_id': results['field_id'],
                'field_number': results['field_number'],
                'booking_status': results['booking_status'],
                'payment_credential_url': results['payment_credential_url'],
                'upload_payment_timestamp': str(results['upload_payment_timestamp']),
                'created_at': str(results['created_at']),
                'booking_creation_age_hour': hours_from_timestamp_to_now(str(results['created_at']))
            }
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

    @app.route('/admin/reservation/status', methods=['PUT'])
    def admin_edit_booking_status():
        token = request.headers['token']
        body = request.json
        if checkAdminToken(token):
            status = body['status']
            if status == 'approved' or status == 'waiting_approval' or status == 'rejected' or status == 'cancelled':
                query = f"UPDATE Reservation SET booking_status = '{status}', last_updated = CURRENT_TIMESTAMP() WHERE id = '{body['reservation_id']}'"
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute(query)
                conn.commit()
                cursor.close()
                conn.close()
                response = {
                    'edit_status': True,
                    'message': f"Reservation {body['reservation_id']}'s booking_status has been updated into {status}",
                    'data': {
                        'reservation_id': body['reservation_id']
                    }
                }
                code = 200
            else:
                response = {
                    'edit_status': False,
                    'message': 'Status is not in the option',
                    'data': None
                }
                code = 400
        else:
            response = {
                'edit_status': False,
                'message': 'Token is expired',
                'data': None
            }
            code = 401

        return jsonify(response), code
