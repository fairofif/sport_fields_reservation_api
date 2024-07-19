import pymysql
from flask import (
    jsonify,
    request
)
from db_config import mysql
from datetime import datetime



def control_system_configure_routes(app):
    def getReservationByFieldDateTime(field_id, date):
        query = f"SELECT Player_username host, name mabar_name, time_start, time_end FROM Reservation WHERE date = '{date}' AND Field_id = '{field_id}' AND booking_status = 'approved'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        results = cursor.fetchall()
        rowcount = cursor.rowcount
        cursor.close()
        conn.close()

        datas = []
        for i in range(rowcount):
            item = {
                'host': results[i]['host'],
                'mabar_name': results[i]['mabar_name'],
                'time_start': str(results[i]['time_start']),
                'time_end': str(results[i]['time_end'])
            }
            datas = datas + [item]
        return datas

    def check_time_interval(time_start, time_end, time_check):
        # Convert time strings to datetime objects
        start = datetime.strptime(time_start, "%H:%M:%S")
        end = datetime.strptime(time_end, "%H:%M:%S")
        check = datetime.strptime(time_check, "%H:%M:%S")

        # Check if time_check is within the interval
        return start <= check <= end

    def get_current_date():
        return datetime.now().strftime("%Y-%m-%d")

    def isReservationExists(reservation_id):
        query = f"SELECT id FROM Reservation WHERE id = '{reservation_id}'"
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

    def isReservationAndVenueMatch(venue_id, reservation_id):
        query = (f"SELECT Sport_Field.id venue_id, Reservation.id reservation_id FROM Reservation "
                + "INNER JOIN Fields ON Reservation.Field_id = Fields.id "
                + "INNER JOIN Sport_Field ON Sport_Field.id = Fields.Sport_Field_id "
                + f"WHERE Reservation.id = '{reservation_id}'"
        )
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result['venue_id'] == venue_id:
            return True
        else:
            return False

    def isCurrentDateMatchWithReservationDate(current_date, reservation_id):
        query = f"SELECT date FROM Reservation WHERE id = '{reservation_id}'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if str(result['date']) == current_date:
            return True
        else:
            return False

    def get_current_time():
        return datetime.now().strftime("%H:%M:%S")

    def is_time_in_interval(time_check, open_time, close_time):
        time_format = "%H:%M:%S"
        time_check_dt = datetime.strptime(time_check, time_format)
        open_time_dt = datetime.strptime(open_time, time_format).time()
        close_time_dt = datetime.strptime(close_time, time_format).time()

        return open_time_dt <= time_check_dt.time() <= close_time_dt

    def isCurrentTimeInsideVenueTimeOpen(venue_id, current_time):
        query = f"SELECT time_open, time_closed FROM Sport_Field WHERE id = '{venue_id}'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        time_open = str(result['time_open'])
        time_closed = str(result['time_closed'])

        return is_time_in_interval(current_time, time_open, time_closed)

    def booking_status(reservation_id):
        query = f"SELECT booking_status FROM Reservation WHERE id = '{reservation_id}'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result['booking_status']

    @app.route('/controlsystem/hostinfo/<field_id>/<date>/<time>', methods=['GET'])
    def get_schedule_host_info(field_id, date, time):
        raw_datas = getReservationByFieldDateTime(field_id, date)
        i = 0
        found = False
        while found == False and i < len(raw_datas):
            found = check_time_interval(raw_datas[i]['time_start'], raw_datas[i]['time_end'], time)
            if found:
                host = raw_datas[i]['host']
                mabar_name = raw_datas[i]['mabar_name']
            i += 1
        if found:
            response = {
                'get_status': True,
                'is_there_a_schedule': True,
                'message': 'There is ongoing schedule',
                'data': {
                    'host': host,
                    'mabar_name': mabar_name
                }
            }
            code = 200
        else:
            response = {
                'get_status': True,
                'is_there_a_schedule': False,
                'message': "There isn't any ongoing schedule",
                'data': None
            }
            code = 200
        return jsonify(response), code

    @app.route('/controlsystem/unlock/<venue_id>/<reservation_id>', methods=['GET'])
    def unlock_venue_door(venue_id, reservation_id):
        if isReservationExists(reservation_id):
            if isReservationAndVenueMatch(venue_id, reservation_id):
                if booking_status(reservation_id) == "approved":
                    if isCurrentDateMatchWithReservationDate(get_current_date(), reservation_id):
                        response = {
                            'unlock_status': True,
                            'message': "Reservation ID is valid, unlock granted",
                            'data': {
                                'reservation_id': reservation_id
                            }
                        }
                        code = 200
                    else:
                        response = {
                            'unlock_status': False,
                            'message': "Reservation ID is not for today, unlock not granted",
                            'data': None
                        }
                        code = 403
                else:
                    response = {
                        'unlock_status': False,
                        'message': "Reservation ID is not approved/not approved yet, unlock not granted",
                        'data': None
                    }
                    code = 403
            else:
                response = {
                    'unlock_status': False,
                    'message': "Reservation ID is not match with this venue, unlock not granted",
                    'data': None
                }
                code = 403
        else:
            response = {
                'unlock_status': False,
                'message': "Reservation ID is not found, unlock not granted",
                'data': None
            }
            code = 404

        return jsonify(response), code