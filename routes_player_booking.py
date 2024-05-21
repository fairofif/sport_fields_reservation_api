import pymysql
from flask import (
    jsonify,
    request
)
from db_config import mysql
from dotenv import load_dotenv
import datetime
import calendar
from uuid_generator import newBookingUUID
import urllib.request
from werkzeug.utils import secure_filename
import os
import haversine as hs
import segno

load_dotenv(override=True)

def player_booking_configure_routes(app):
    # ==== SETUP ===== #
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER_PAYMENT")
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = set(['heic', 'jpg', 'jpeg', 'png', 'gif'])
    BASE_URL_IMAGE = os.getenv("BASE_URL_IMAGE")

    FOLDER_QR = os.getenv("FOLDER_QR")

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


    # ============ Static Methods ================== #
    def calculateHourFrom2Times(start_time_str, end_time_str):
        # Parse time strings to datetime objects
        start_time = datetime.datetime.strptime(start_time_str, "%H:%M:%S")
        end_time = datetime.datetime.strptime(end_time_str, "%H:%M:%S")

        # Calculate the time difference
        time_difference = end_time - start_time

        # Round up to the nearest hour
        hours = (time_difference.total_seconds() + 3600 - 1) // 3600

        return int(hours)

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

    def get_current_time_string():
        current_time = datetime.datetime.now().time()
        formatted_time = current_time.strftime('%H%M%S%f')[:-3]  # Exclude microseconds
        return formatted_time

    def check_2_schedule_conflict(time_start, time_end, time_start_compare, time_end_compare):
        # Convert string times to datetime objects
        start = datetime.datetime.strptime(time_start, '%H:%M:%S')
        end = datetime.datetime.strptime(time_end, '%H:%M:%S')
        start_compare = datetime.datetime.strptime(time_start_compare, '%H:%M:%S')
        end_compare = datetime.datetime.strptime(time_end_compare, '%H:%M:%S')

        # Check for conflicts
        if (start <= start_compare and end >= start_compare) or \
        (start <= end_compare and end >= end_compare) or \
        (start >= start_compare and end <= end_compare):
            return True  # Conflict exists
        else:
            return False  # No conflict

    def check_2_schedule_is_out_of_range(time_start, time_end, time_open, time_closed):
        # Convert string times to datetime objects
        start = datetime.datetime.strptime(time_start, '%H:%M:%S').time()
        end = datetime.datetime.strptime(time_end, '%H:%M:%S').time()
        open_time = datetime.datetime.strptime(time_open, '%H:%M:%S').time()
        closed_time = datetime.datetime.strptime(time_closed, '%H:%M:%S').time()

        # Check if the schedule is within the open and closed times
        if start < open_time or end > closed_time:
            return True  # Schedule is out of range
        else:
            return False  # Schedule is within range

    def isScheduleNotConflictWithOtherBook(field_id, date, time_start, time_end):
        query = f"SELECT id, Field_id, date, time_start, time_end FROM Reservation WHERE Field_id = '{field_id}' AND date = '{date}'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        results = cursor.fetchall()

        count_conflict = 0
        i = 0
        while count_conflict == 0 and i < cursor.rowcount:
            if check_2_schedule_conflict(time_start, time_end, str(results[i]['time_start']), str(results[i]['time_end'])):
                count_conflict += 1
            i += 1
        cursor.close()
        conn.close()
        if count_conflict == 0:
            return True
        else:
            return False

    def isScheduleNotConflictWithVenueOpenTime(venue_id, time_start, time_end):
        query = f"SELECT time_open, time_closed FROM Sport_Field WHERE id = '{venue_id}'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        return not check_2_schedule_is_out_of_range(time_start, time_end, str(result['time_open']), str(result['time_closed']))

    def isThereAnyBlacklistSchedule(field_id):
        query = f"SELECT * FROM Blacklist_Schedule WHERE Field_id = '{field_id}'"
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

    def getBlackListScheduleFromMonthAndYear(field_id, month, year):
        if isThereAnyBlacklistSchedule(field_id):
            data = []
            query = f"SELECT id blacklist_id, date, fromTime, toTime, reason FROM Blacklist_Schedule WHERE Field_id = '{field_id}' AND MONTH(date) = {month} AND YEAR(date) = {year} AND is_every_week = 0"
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            query_resp = cursor.fetchall()
            for i in range(cursor.rowcount):
                item = {
                    "blacklist_id": query_resp[i]['blacklist_id'],
                    "date": str(query_resp[i]['date']),
                    "fromTime": str(query_resp[i]['fromTime']),
                    "toTime": str(query_resp[i]['toTime']),
                    "reason": query_resp[i]['reason']
                }
                data = data + [item]
            cursor.close()
            conn.close()

            query = f"SELECT id blacklist_id, date, fromTime, toTime, reason FROM Blacklist_Schedule WHERE Field_id = '{field_id}' AND is_every_week = 1"
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            if cursor.rowcount != 0:
                query_resp = cursor.fetchall()
                for i in range(cursor.rowcount):
                    format_date = datetime.datetime.strptime(str(query_resp[i]['date']), "%Y-%m-%d")
                    day_date = format_date.strftime("%A")
                    if format_date.month == month and format_date.year == year:
                        num_days = calendar.monthrange(year, month)[1]
                        date_in_a_month = [datetime.date(year, month, day) for day in range(1, num_days+1)]
                        for j in range(len(date_in_a_month)):
                            if date_in_a_month[j].day >= format_date.day and date_in_a_month[j].strftime("%A") == day_date:
                                item = {
                                    "blacklist_id": str(query_resp[i]['blacklist_id']),
                                    "date": str(date_in_a_month[j].strftime('%Y-%m-%d')),
                                    "fromTime": str(query_resp[i]['fromTime']),
                                    "toTime": str(query_resp[i]['toTime']),
                                    "reason": str(query_resp[i]['reason'])
                                    }
                                data = data + [item]
                    elif (format_date.month < month and format_date.year <= year) or (format_date.month >= month and format_date.year < year):
                        num_days = calendar.monthrange(year, month)[1]
                        date_in_a_month = [datetime.date(year, month, day) for day in range(1, num_days+1)]
                        for j in range(len(date_in_a_month)):
                            if date_in_a_month[j].strftime("%A") == day_date:
                                item = {
                                    "blacklist_id": str(query_resp[i]['blacklist_id']),
                                    "date": str(date_in_a_month[j].strftime('%Y-%m-%d')),
                                    "fromTime": str(query_resp[i]['fromTime']),
                                    "toTime": str(query_resp[i]['toTime']),
                                    "reason": str(query_resp[i]['reason'])
                                    }
                                data = data + [item]
            cursor.close()
            conn.close()
            return data
        else:
            return []

    def extract_month_and_year(date_string):
        # Convert string date to datetime object
        date_object = datetime.datetime.strptime(date_string, '%Y-%m-%d')

        # Extract month and year as integers
        day = date_object.day
        month = date_object.month
        year = date_object.year

        return day, month, year

    def isScheduleNotConflictWithBlacklistSchedule(field_id, date, time_start, time_end):
        day, month, year = extract_month_and_year(date)
        blacklist = getBlackListScheduleFromMonthAndYear(field_id, month, year)

        count_conflict = 0
        i = 0
        while count_conflict == 0 and i < len(blacklist):
            # check date #
            inner_day, inner_month, inner_year = extract_month_and_year(blacklist[i]['date'])
            if day == inner_day and month == inner_month and year == inner_year:
                if check_2_schedule_conflict(time_start, time_end, blacklist[i]['fromTime'], blacklist[i]['toTime']):
                    count_conflict += 1
            i += 1

        if count_conflict == 0:
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

    def convertCoordinate(loc_string):
        lat_str, lon_str = loc_string.split(',')
        lat = float(lat_str.strip())
        lon = float(lon_str.strip())

        return (lat, lon)

    def calculateDistance(loc1_str, loc2_str):
        loc1 = convertCoordinate(loc1_str)
        loc2 = convertCoordinate(loc2_str)

        return hs.haversine(loc1, loc2)

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

    def reservationBookingStatus(reservation_id):
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

    def isQRAlreadyExists(reservation_id):
        query = f"SELECT Reservation_id FROM Reservation_QR WHERE Reservation_id = '{reservation_id}'"
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

    def is_public_status(reservation_id):
        query = f"SELECT is_public FROM Reservation WHERE id = '{reservation_id}'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result['is_public']

    def isPlayerHasAReservation(username):
        query = f"SELECT id FROM Reservation WHERE Player_username = '{username}'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        rows = cursor.rowcount
        cursor.close()
        conn.close()

        if rows > 0:
            return True
        else:
            return False

    # =================== ROUTES ===================== #
    @app.route('/player/reservation', methods=['POST'])
    def player_create_booking():
        token = request.headers['token']
        body = request.json
        field_id = body['field_id']
        query = f"SELECT Sport_Field_id FROM Fields WHERE id = '{field_id}'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        query_resp = cursor.fetchone()
        cursor.close()
        conn.close()

        venue_id = query_resp['Sport_Field_id']
        date = body['date']
        time_start = body['time_start']
        time_end = body['time_end']
        if checkPlayerToken(token):
            username = findUsernameFromToken(token)
            if isScheduleNotConflictWithVenueOpenTime(venue_id, time_start, time_end):
                if isScheduleNotConflictWithOtherBook(field_id, date, time_start, time_end):
                    if isScheduleNotConflictWithBlacklistSchedule(field_id, date, time_start, time_end):
                        booking_id = newBookingUUID()
                        query = "INSERT INTO Reservation (id, Field_id, Player_username, name, mabar_type, date, time_start, time_end, created_at, last_updated) VALUES "
                        query = query + f"('{booking_id}', '{field_id}', '{username}', '{body['name']}', '{body['mabar_type']}', '{date}', '{time_start}', '{time_end}', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP())"
                        conn = mysql.connect()
                        cursor = conn.cursor(pymysql.cursors.DictCursor)
                        cursor.execute(query)
                        conn.commit()

                        query = f"SELECT id, Field_id, Player_username, name, mabar_type, date, time_start, time_end, booking_status, payment_credential_url, is_public, is_open_member FROM Reservation WHERE id = '{booking_id}'"
                        cursor.execute(query)
                        data = cursor.fetchone()
                        cursor.close()
                        conn.close()

                        code = 200
                        response = {
                            'create_status': True,
                            'message': "Create booking successfully",
                            'data': {
                                'id': data['id'],
                                'Field_id': data['Field_id'],
                                'Player_username': data['Player_username'],
                                'name': data['name'],
                                'mabar_type': data['mabar_type'],
                                'date': str(data['date']),
                                'time_start': str(data['time_start']),
                                'time_end': str(data['time_end']),
                                'booking_status': data['booking_status'],
                                'payment_credential_url': data['payment_credential_url'],
                                'is_public': bool(data['is_public']),
                                'is_open_member': bool(data['is_open_member'])
                            }
                        }
                    else:
                        code = 409
                        response = {
                            'create_status': False,
                            'message': 'Schedule that you choose is blaklisted by admin',
                            'data': None
                        }
                else:
                    code = 409
                    response = {
                        'create_status': False,
                        'message': 'Schedule that you choose is taken by others',
                        'data': None
                    }
            else:
                code = 409
                response = {
                    'create_status': False,
                    'message': "Schedule that you choose is out of range of this venue's open-closed time",
                    'data': None
                }
        else:
            code = 401
            response = {
                'create_status': False,
                'message': 'Token is Expired',
                'data': None
            }
        return jsonify(response), code


    @app.route('/player/reservation/upload/<reservation_id>', methods=['POST'])
    def player_uploads_payment(reservation_id):
        token = request.headers['token']
        if checkPlayerToken(token):
            username = findUsernameFromToken(token)
            if 'file' not in request.files:
                response = {
                    'upload_status': False,
                    'message': 'No file part in request',
                    'data': None
                }
                code = 400
            else:
                image = request.files['file']

                if image.filename == '':
                    response = {
                        'upload_status': False,
                        'message': 'No selected file',
                        'data': None
                    }
                    code = 400
                else:
                    if image and allowed_file(image.filename):
                        file_extension = image.filename.rsplit('.', 1)[1].lower()
                        custom_filename = f"{username}_{reservation_id}_{get_current_time_string()}."
                        filename = custom_filename+file_extension
                        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        url_image = f"{BASE_URL_IMAGE}/payments/{filename}"

                        query = f"UPDATE Reservation SET payment_credential_url = '{url_image}', last_updated = CURRENT_TIMESTAMP(), booking_status = 'waiting_approval', upload_payment_timestamp = CURRENT_TIMESTAMP() WHERE id = '{reservation_id}'"
                        conn = mysql.connect()
                        cursor = conn.cursor(pymysql.cursors.DictCursor)
                        cursor.execute(query)
                        conn.commit()
                        cursor.close()
                        conn.close()

                        response = {
                            'upload_status': True,
                            'message': 'Upload file successfully',
                            'data': {
                                'url_image': url_image
                            }
                        }
                        code = 201
                    else:
                        response = {
                            'upload_status': False,
                            'message': 'Extensions file is not allowed',
                            'data': None
                        }
                        code = 400
        else:
            response = {
                'upload_status': False,
                'messagge': 'Token is expired',
                'data': None
            }
            code = 401
        return jsonify(response), code

    @app.route('/player/reservation/cancel/<reservation_id>', methods=['PUT'])
    def player_cancel_reservation(reservation_id):
        token = request.headers['token']
        if checkPlayerToken(token):
            query = f"SELECT booking_status FROM Reservation WHERE id = '{reservation_id}'"
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            result = cursor.fetchone()
            if result['booking_status'] == 'payment' or result['booking_status'] == 'waiting_approval':
                query = f"UPDATE Reservation SET booking_status = 'cancelled' WHERE id = '{reservation_id}'"
                cursor.execute(query)
                conn.commit()
                response = {
                    'edit_status': True,
                    'message': f"Reservation {reservation_id} has been cancelled successfully",
                    'data': {
                        'reservation_id': reservation_id
                    }
                }
                code = 200
            else:
                response = {
                    'edit_status': False,
                    'message': f"Reservation with booking_status = '{result['booking_status']}' cannot be cancelled",
                    'data': None
                }
                code = 403
            cursor.close()
            conn.close()
        else:
            response = {
                'edit_status': False,
                'message': 'Token is expired',
                'data': None
            }
            code = 401

        return jsonify(response), code

    @app.route('/player/reservation/open/<reservation_id>/<is_open_member>', methods=['PUT'])
    def change_open_member_status(reservation_id, is_open_member):
        token = request.headers['token']
        if checkPlayerToken(token):
            username = findUsernameFromToken(token)
            if usernameIsAHost(username, reservation_id):
                if is_open_member == '1':
                    booking_status = findBookingStatusOfReservation(reservation_id)
                    if booking_status == 'approved':
                        query = f"UPDATE Reservation SET is_open_member = {is_open_member} WHERE id = '{reservation_id}'"
                        conn = mysql.connect()
                        cursor = conn.cursor(pymysql.cursors.DictCursor)
                        cursor.execute(query)
                        conn.commit()
                        cursor.close()
                        conn.close()
                        response = {
                            'edit_status': True,
                            'message': f"Reservation {reservation_id} now is open member",
                            'data': {
                                'reservation_id': reservation_id
                            }
                        }
                        code = 200
                    else:
                        response = {
                            'edit_status': False,
                            'message': 'Only approved reservation could open member',
                            'data': None
                        }
                        code = 403
                else:
                    query = f"UPDATE Reservation SET is_open_member = {is_open_member} WHERE id = '{reservation_id}'"
                    conn = mysql.connect()
                    cursor = conn.cursor(pymysql.cursors.DictCursor)
                    cursor.execute(query)
                    conn.commit()
                    cursor.close()
                    conn.close()
                    response = {
                        'edit_status': True,
                        'message': f"Reservation {reservation_id} now is closed member",
                        'data': {
                            'reservation_id': reservation_id
                        }
                    }
                    code = 200
            else:
                response = {
                    'edit_status': False,
                    'message': 'Only host could edit open member status of reservation',
                    'data': None
                }
                code = 401
        else:
            response = {
                'edit_status': False,
                'message': 'Token is expired',
                'data': None
            }
            code = 401

        return jsonify(response), code

    @app.route('/player/reservation/public/<reservation_id>/<is_public>', methods=['PUT'])
    def change_public_status(reservation_id, is_public):
        token = request.headers['token']
        if checkPlayerToken(token):
            username = findUsernameFromToken(token)
            if usernameIsAHost(username, reservation_id):
                if is_public == '1':
                    booking_status = findBookingStatusOfReservation(reservation_id)
                    if booking_status == 'approved':
                        query = f"UPDATE Reservation SET is_public = {is_public} WHERE id = '{reservation_id}'"
                        conn = mysql.connect()
                        cursor = conn.cursor(pymysql.cursors.DictCursor)
                        cursor.execute(query)
                        conn.commit()
                        cursor.close()
                        conn.close()
                        response = {
                            'edit_status': True,
                            'message': f"Reservation {reservation_id} now is public",
                            'data': {
                                'reservation_id': reservation_id
                            }
                        }
                        code = 200
                    else:
                        response = {
                            'edit_status': False,
                            'message': 'Only approved reservation could public',
                            'data': None
                        }
                        code = 403
                else:
                    query = f"UPDATE Reservation SET is_public = {is_public} WHERE id = '{reservation_id}'"
                    conn = mysql.connect()
                    cursor = conn.cursor(pymysql.cursors.DictCursor)
                    cursor.execute(query)
                    conn.commit()
                    cursor.close()
                    conn.close()
                    response = {
                        'edit_status': True,
                        'message': f"Reservation {reservation_id} now is unpublic",
                        'data': {
                            'reservation_id': reservation_id
                        }
                    }
                    code = 200
            else:
                response = {
                    'edit_status': False,
                    'message': 'Only host could edit public status of reservation',
                    'data': None
                }
                code = 401
        else:
            response = {
                'edit_status': False,
                'message': 'Token is expired',
                'data': None
            }
            code = 401

        return jsonify(response), code

    @app.route('/player/reservation/public/<sport_kind_id>/<mabar_type>/<sort_by>', methods=['GET'])
    def get_public_reservation_by_filters(sport_kind_id, mabar_type, sort_by):
        token = request.headers['token']
        if checkPlayerToken(token):
            query_init = (
                "SELECT Sport_Field.id venue_id, Sport_Field.name venue_name, "
                + "Sport_Kind.id sport_kind_id, Fields.id field_id, Fields.number field_number, "
                + "Sport_Kind.name sport_kind_name, Reservation.id reservation_id, Reservation.is_open_member is_open_member, Reservation.Player_username host_name, "
                + "Reservation.name mabar_name, Reservation.date playing_date, Reservation.time_start, "
                + "Reservation.time_end, Sport_Field.geo_coordinate, COUNT(Reservation_Member.Player_username) count_member FROM Sport_Field "
                + "INNER JOIN Fields ON (Sport_Field.id = Fields.Sport_Field_id) "
                + "INNER JOIN Sport_Kind ON (Sport_Field.Sport_Kind_id = Sport_Kind.id) "
                + "INNER JOIN Reservation ON (Fields.id = Reservation.Field_id) "
                + "LEFT JOIN Reservation_Member ON (Reservation.id = Reservation_Member.Reservation_id) "
            )
            filters = []
            filters = filters + ["Reservation.is_public = 1"]
            if sport_kind_id != 'all':
                filters = filters + [f"Sport_Kind.id = '{sport_kind_id}'"]
            if mabar_type != 'all':
                filters = filters + [f"Reservation.mabar_type = '{mabar_type}'"]
            for i in range(len(filters)):
                if i == 0:
                    query_init = query_init + 'WHERE ' + filters[i] + ' '
                else:
                    query_init = query_init + 'AND ' + filters[i] + ' '
            query_init = query_init + 'GROUP BY Reservation.id '
            if sort_by == 'date':
                query_final = query_init + 'ORDER BY playing_date, time_start '
            else:
                query_final = query_init

            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query_final)
            results = cursor.fetchall()
            rowcount = cursor.rowcount
            cursor.close()
            conn.close()
            datas = []

            if request.headers.get('geo_coordinate') != None and request.headers.get('geo_coordinate') != "":
                geo_coordinate = request.headers['geo_coordinate']
                for i in range(rowcount):
                    data = {
                        'reservation_id': results[i]['reservation_id'],
                        'host_name': results[i]['host_name'],
                        'mabar_name': results[i]['mabar_name'],
                        'playing_date': str(results[i]['playing_date']),
                        'time_start': str(results[i]['time_start']),
                        'time_end': str(results[i]['time_end']),
                        'distance': calculateDistance(geo_coordinate, str(results[i]['geo_coordinate'])),
                        'venue_id': results[i]['venue_id'],
                        'venue_name': results[i]['venue_name'],
                        'sport_kind_id': results[i]['sport_kind_id'],
                        'sport_kind_name': results[i]['sport_kind_name'],
                        'field_id': results[i]['field_id'],
                        'field_number': results[i]['field_number'],
                        'count_member': results[i]['count_member'] + 1,
                        'is_open_member': bool(results[i]['is_open_member'])
                    }
                    datas = datas + [data]
            else:
                for i in range(rowcount):
                    data = {
                        'reservation_id': results[i]['reservation_id'],
                        'host_name': results[i]['host_name'],
                        'mabar_name': results[i]['mabar_name'],
                        'playing_date': str(results[i]['playing_date']),
                        'time_start': str(results[i]['time_start']),
                        'time_end': str(results[i]['time_end']),
                        'distance': None,
                        'venue_id': results[i]['venue_id'],
                        'venue_name': results[i]['venue_name'],
                        'sport_kind_id': results[i]['sport_kind_id'],
                        'sport_kind_name': results[i]['sport_kind_name'],
                        'field_id': results[i]['field_id'],
                        'field_number': results[i]['field_number'],
                        'count_member': results[i]['count_member'] + 1,
                        'is_open_member': bool(results[i]['is_open_member'])
                    }
                    datas = datas + [data]
            if sort_by == 'distance' and request.headers.get('geo_coordinate') != None and request.headers.get('geo_coordinate') != "":
                datas = sorted(datas, key=lambda x: x['distance'])

            response = {
                'get_status': True,
                'message': 'Retrieve public reservation success',
                'data': datas
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

    @app.route('/player/reservation/<booking_status>', methods=['GET'])
    def get_user_reservation_with_booking_status(booking_status):
        token = request.headers['token']
        if checkPlayerToken(token):
            username = findUsernameFromToken(token)
            if isPlayerHasAReservation(username):
                if booking_status == 'all':
                    query = (
                        "SELECT Sport_Field.id venue_id, Sport_Field.name venue_name, "
                        + "Sport_Kind.id sport_kind_id, Fields.id field_id, Fields.number field_number, "
                        + "Sport_Kind.name sport_kind_name, Reservation.id reservation_id, Reservation.is_open_member is_open_member, Reservation.Player_username host_name, "
                        + "Reservation.name mabar_name, Reservation.date playing_date, Reservation.time_start, Reservation.created_at booking_created_at, "
                        + "Reservation.time_end, Reservation.booking_status, Sport_Field.geo_coordinate, COUNT(Reservation_Member.Player_username) count_member FROM Sport_Field "
                        + "INNER JOIN Fields ON (Sport_Field.id = Fields.Sport_Field_id) "
                        + "INNER JOIN Sport_Kind ON (Sport_Field.Sport_Kind_id = Sport_Kind.id) "
                        + "INNER JOIN Reservation ON (Fields.id = Reservation.Field_id) "
                        + "LEFT JOIN Reservation_Member ON (Reservation.id = Reservation_Member.Reservation_id) "
                        + f"WHERE Reservation.Player_username = '{username}' "
                        + "GROUP BY Reservation.id ORDER BY Reservation.created_at DESC"
                    )
                else:
                    query = (
                        "SELECT Sport_Field.id venue_id, Sport_Field.name venue_name, "
                        + "Sport_Kind.id sport_kind_id, Fields.id field_id, Fields.number field_number, "
                        + "Sport_Kind.name sport_kind_name, Reservation.id reservation_id, Reservation.is_open_member is_open_member, Reservation.Player_username host_name, "
                        + "Reservation.name mabar_name, Reservation.date playing_date, Reservation.time_start, Reservation.created_at booking_created_at, "
                        + "Reservation.time_end, Reservation.booking_status, Sport_Field.geo_coordinate, COUNT(Reservation_Member.Player_username) count_member FROM Sport_Field "
                        + "INNER JOIN Fields ON (Sport_Field.id = Fields.Sport_Field_id) "
                        + "INNER JOIN Sport_Kind ON (Sport_Field.Sport_Kind_id = Sport_Kind.id) "
                        + "INNER JOIN Reservation ON (Fields.id = Reservation.Field_id) "
                        + "LEFT JOIN Reservation_Member ON (Reservation.id = Reservation_Member.Reservation_id) "
                        + f"WHERE Reservation.Player_username = '{username}' AND Reservation.booking_status = '{booking_status}' "
                        + "GROUP BY Reservation.id ORDER BY Reservation.created_at DESC"
                    )

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
                        'reservation_id': results[i]['reservation_id'],
                        'host_name': results[i]['host_name'],
                        'mabar_name': results[i]['mabar_name'],
                        'playing_date': str(results[i]['playing_date']),
                        'time_start': str(results[i]['time_start']),
                        'time_end': str(results[i]['time_end']),
                        'booking_status': results[i]['booking_status'],
                        'venue_id': results[i]['venue_id'],
                        'venue_name': results[i]['venue_name'],
                        'sport_kind_id': results[i]['sport_kind_id'],
                        'sport_kind_name': results[i]['sport_kind_name'],
                        'field_id': results[i]['field_id'],
                        'field_number': results[i]['field_number'],
                        'count_member': results[i]['count_member'] + 1,
                        'is_open_member': bool(results[i]['is_open_member'])
                    }
                    datas = datas + [item]

                response = {
                    'get_status': True,
                    'message': "Retrieve user reservation success",
                    'data': datas
                }
                code = 200

            else:
                response = {
                    'get_status': False,
                    'message': "Player have not been created any reservation",
                    'data': None
                }
                code = 404
        else:
            response = {
                'get_status': False,
                'message': "Token is expired",
                'data': None
            }
            code = 401

        return jsonify(response), code

    @app.route('/player/reservation/joined/<sport_kind_id>', methods=['GET'])
    def get_joined_reservation(sport_kind_id):
        token = request.headers['token']
        if checkPlayerToken(token):
            username = findUsernameFromToken(token)
            if sport_kind_id == 'all':
                query = (
                    "SELECT Sport_Field.id venue_id, Sport_Field.name venue_name, "
                    + "Sport_Kind.id sport_kind_id, Fields.id field_id, Fields.number field_number, "
                    + "Sport_Kind.name sport_kind_name, Reservation.id reservation_id, Reservation.is_open_member is_open_member, Reservation.Player_username host_name, "
                    + "Reservation.name mabar_name, Reservation.date playing_date, Reservation.time_start, Reservation.created_at booking_created_at, "
                    + "Reservation.time_end, Sport_Field.geo_coordinate, COUNT(Reservation_Member.Player_username) count_member FROM Sport_Field "
                    + "INNER JOIN Fields ON (Sport_Field.id = Fields.Sport_Field_id) "
                    + "INNER JOIN Sport_Kind ON (Sport_Field.Sport_Kind_id = Sport_Kind.id) "
                    + "INNER JOIN Reservation ON (Fields.id = Reservation.Field_id) "
                    + "LEFT JOIN Reservation_Member ON (Reservation.id = Reservation_Member.Reservation_id) "
                    + f"WHERE Reservation_Member.Player_username = '{username}' "
                    + "GROUP BY Reservation.id ORDER BY Reservation.created_at DESC"
                )
            else:
                query = (
                    "SELECT Sport_Field.id venue_id, Sport_Field.name venue_name, "
                    + "Sport_Kind.id sport_kind_id, Fields.id field_id, Fields.number field_number, "
                    + "Sport_Kind.name sport_kind_name, Reservation.id reservation_id, Reservation.is_open_member is_open_member, Reservation.Player_username host_name, "
                    + "Reservation.name mabar_name, Reservation.date playing_date, Reservation.time_start, Reservation.created_at booking_created_at, "
                    + "Reservation.time_end, Sport_Field.geo_coordinate, COUNT(Reservation_Member.Player_username) count_member FROM Sport_Field "
                    + "INNER JOIN Fields ON (Sport_Field.id = Fields.Sport_Field_id) "
                    + "INNER JOIN Sport_Kind ON (Sport_Field.Sport_Kind_id = Sport_Kind.id) "
                    + "INNER JOIN Reservation ON (Fields.id = Reservation.Field_id) "
                    + "LEFT JOIN Reservation_Member ON (Reservation.id = Reservation_Member.Reservation_id) "
                    + f"WHERE Reservation_Member.Player_username = '{username}' AND Sport_Kind.id = '{sport_kind_id}'"
                    + "GROUP BY Reservation.id ORDER BY Reservation.created_at DESC"
                )

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
                    'reservation_id': results[i]['reservation_id'],
                    'host_name': results[i]['host_name'],
                    'mabar_name': results[i]['mabar_name'],
                    'playing_date': str(results[i]['playing_date']),
                    'time_start': str(results[i]['time_start']),
                    'time_end': str(results[i]['time_end']),
                    'venue_id': results[i]['venue_id'],
                    'venue_name': results[i]['venue_name'],
                    'sport_kind_id': results[i]['sport_kind_id'],
                    'sport_kind_name': results[i]['sport_kind_name'],
                    'field_id': results[i]['field_id'],
                    'field_number': results[i]['field_number'],
                    'count_member': results[i]['count_member'] + 1,
                    'is_open_member': bool(results[i]['is_open_member'])
                }
                datas = datas + [item]

            if rowcount > 0:
                response = {
                    'get_status': True,
                    'message': "Retrieve joined reservation success",
                    'data': datas
                }
                code = 200
            else:
                response = {
                    'get_status': False,
                    'message': "Player has not been joined any reservation / or has not been joined reservation with that sport_kind_id",
                    'data': None
                }
                code = 404
        else:
            response = {
                'get_status': False,
                'message': "Token is expired",
                'data': None
            }
            code = 401
        return jsonify(response), code

    @app.route('/player/reservation/details/<reservation_id>', methods=['GET'])
    def get_reservation_details_by_player(reservation_id):
        token = request.headers['token']
        if checkPlayerToken(token):
            username = findUsernameFromToken(token)
            if isReservationExists(reservation_id):
                is_host = not isPlayerNotAHost(reservation_id, username)
                is_member = not isPlayerNotAlreadyInAReservationAsMember(reservation_id, username)
                if is_host or is_member:
                    query = (
                        "SELECT Sport_Field.Admin_username, Sport_Field.id venue_id, Sport_Field.name venue_name, "
                        + "Sport_Field.price_per_hour, Sport_Kind.id sport_kind_id, Fields.id field_id, Fields.number field_number, "
                        + "Sport_Kind.name sport_kind_name, Reservation.id reservation_id, Reservation.is_open_member is_open_member, Reservation.Player_username host_name, Reservation.name mabar_name, "
                        + "Reservation.is_public is_public, Reservation.date playing_date, Reservation.time_start, Reservation.time_end, Reservation.booking_status, "
                        + "Reservation.created_at FROM Sport_Field "
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
                    item = {
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
                        'created_at': str(results['created_at']),
                        'is_public': results['is_public'],
                        'is_open_member': results['is_open_member']
                    }

                    if is_host:
                        role = "host"
                    else:
                        role = "member"

                    response = {
                        'get_status': True,
                        'message': 'Retrieve reservation info successfully',
                        'data': {
                            'role': role,
                            'info': item
                        }
                    }
                    code = 200
                else:
                    if is_public_status(reservation_id):
                        query = (
                            "SELECT Sport_Field.Admin_username, Sport_Field.id venue_id, Sport_Field.name venue_name, "
                            + "Sport_Field.price_per_hour, Sport_Kind.id sport_kind_id, Fields.id field_id, Fields.number field_number, "
                            + "Sport_Kind.name sport_kind_name, Reservation.id reservation_id, Reservation.is_open_member is_open_member, Reservation.Player_username host_name, Reservation.name mabar_name, "
                            + "Reservation.is_public is_public, Reservation.date playing_date, Reservation.time_start, Reservation.time_end, Reservation.booking_status, "
                            + "Reservation.created_at FROM Sport_Field "
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
                        item = {
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
                            'created_at': str(results['created_at']),
                            'is_public': results['is_public'],
                            'is_open_member': results['is_open_member']
                        }
                        role = "guest"
                        response = {
                            'get_status': True,
                            'message': 'Retrieve reservation info successfully',
                            'data': {
                                'role': role,
                                'info': item
                            }
                        }
                        code = 200
                    else:
                        response = {
                            'get_status': False,
                            'message': 'Retrieve reservation info unsuccessfully',
                            'data': {
                                'role': None,
                                'info': None
                            }
                        }
                        code = 403
            else:
                response = {
                    'get_status': False,
                    'message': f"Reservation {reservation_id} is not found",
                    'data': {
                        'role': None,
                        'info': None
                    }
                }
                code = 404
        else:
            response = {
                'get_status': False,
                'message': 'Token is expired',
                'data': {
                    'role': None,
                    'info': None
                }
            }
            code = 401
        return jsonify(response), code

    @app.route('/player/reservation/QR/<reservation_id>', methods=['POST'])
    def get_post_qr_reservation(reservation_id):
        token = request.headers['token']
        if checkPlayerToken(token):
            username = findUsernameFromToken(token)
            if isReservationExists(reservation_id):
                if not isPlayerNotAHost(reservation_id, username) or not isPlayerNotAlreadyInAReservationAsMember(reservation_id, username):
                    if reservationBookingStatus(reservation_id) == "approved":
                        if isQRAlreadyExists(reservation_id):
                            query = f"SELECT * FROM Reservation_QR WHERE Reservation_id = '{reservation_id}'"
                            conn = mysql.connect()
                            cursor = conn.cursor(pymysql.cursors.DictCursor)
                            cursor.execute(query)
                            result = cursor.fetchone()
                            cursor.close()
                            conn.close()

                            response = {
                                'get_status': True,
                                'message': 'QR had created before, get QR successfully',
                                'data': {
                                    'url_qr': result['url']
                                }
                            }
                            code = 200
                        else:
                            qr = segno.make_qr(reservation_id)
                            qr.save(
                                f"{FOLDER_QR}/{reservation_id}.png",
                                scale = 30
                            )
                            url = f"{BASE_URL_IMAGE}/qr/{reservation_id}.png"
                            query = f"INSERT INTO Reservation_QR VALUES ('{reservation_id}', '{url}')"
                            conn = mysql.connect()
                            cursor = conn.cursor(pymysql.cursors.DictCursor)
                            cursor.execute(query)
                            conn.commit()
                            cursor.close()
                            conn.close()

                            response = {
                                'get_status': True,
                                'message': 'New QR Created successfully',
                                'data': {
                                    'url_qr': url
                                }
                            }
                            code = 200
                    else:
                        response = {
                            'get_status': False,
                            'message': f"Reservation {reservation_id} not approved yet",
                            'data': None
                        }
                        code = 403
                else:
                    response = {
                        'get_status': False,
                        'message': f"This user is not host or member of reservation {reservation_id}",
                        'data': None
                    }
                    code = 403
            else:
                response = {
                    'get_status': False,
                    'message': f"Reservation {reservation_id} is not found",
                    'data': None
                }
                code = 404
        else:
            response = {
                'get_status': False,
                'message': f"Token is expired",
                'data': None
            }
            code = 401
        return jsonify(response), code
