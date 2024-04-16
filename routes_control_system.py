import pymysql
from flask import (
    jsonify,
    request
)
from db_config import mysql
from datetime import datetime



def control_system_configure_routes(app):
    def getReservationByFieldDateTime(field_id, date):
        query = f"SELECT Player_username host, name mabar_name, time_start, time_end FROM Reservation WHERE date = '{date}' AND Field_id = '{field_id}'"
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
