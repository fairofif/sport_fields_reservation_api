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

load_dotenv(override=True)

def player_booking_configure_routes(app):
    # ============ Static Methods ================== #
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
        month = date_object.month
        year = date_object.year

        return month, year

    def isScheduleNotConflictWithBlacklistSchedule(field_id, date, time_start, time_end):
        month, year = extract_month_and_year(date)
        blacklist = getBlackListScheduleFromMonthAndYear(field_id, month, year)

        count_conflict = 0
        i = 0
        while count_conflict == 0 and i < len(blacklist):
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

    # =================== ROUTES ===================== #
    @app.route('/player/booking', methods=['POST'])
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

        username = findUsernameFromToken(token)

        venue_id = query_resp['Sport_Field_id']
        date = body['date']
        time_start = body['time_start']
        time_end = body['time_end']
        if checkPlayerToken(token):
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