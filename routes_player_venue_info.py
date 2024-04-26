import pymysql
from flask import (
    jsonify,
    request
)
from db_config import mysql
from dotenv import load_dotenv
import datetime
import calendar
import haversine as hs
load_dotenv(override=True)

def player_venue_info_cofigure_routes(app):
    # ======================= STATIC METHODS ======================== #
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

    def convertCoordinate(loc_string):
        lat_str, lon_str = loc_string.split(',')
        lat = float(lat_str.strip())
        lon = float(lon_str.strip())

        return (lat, lon)

    def calculateDistance(loc1_str, loc2_str):
        loc1 = convertCoordinate(loc1_str)
        loc2 = convertCoordinate(loc2_str)

        return hs.haversine(loc1, loc2)

    def isSportVenueExist(venue_id):
        query = "SELECT * FROM Sport_Field WHERE id = '"+venue_id+"'"
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

    def isVenuePublic(venue_id):
        query = f"SELECT is_public FROM Sport_Field WHERE id = '{venue_id}'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        result = cursor.fetchone()
        return bool(result['is_public'])
    # ====================== ROUTES ======================= #

    @app.route('/player/sportVenue', methods=['POST'])
    def get_sport_venue_list():
        header = request.headers
        body = request.json
        token = header['token']
        if checkPlayerToken(token):
            array_condition = ['is_car_parking', 'is_bike_parking', 'name', 'Sport_Kind_id']
            query_condition = "WHERE "
            for i in range(len(array_condition)):
                if body[array_condition[i]] != None:
                    if array_condition[i] == 'name':
                        query_condition = query_condition + f"Sport_Field.name LIKE '%{body[array_condition[i]]}%' AND "
                    elif array_condition[i] == 'Sport_Kind_id':
                        query_condition = query_condition + f"Sport_Field.Sport_Kind_id = '{body[array_condition[i]]}' AND "
                    else:
                        query_condition = query_condition + f"Sport_Field.{array_condition[i]} = {str(int(body[array_condition[i]]))} AND "

            query_condition = query_condition + "Sport_Field.is_public = 1 "

            query = ("SELECT Sport_Field.id, Sport_Field.Sport_Kind_id, Sport_Kind.name Sport_Kind_Name, Sport_Field.name, "
                        +"Sport_Field.created_at, Sport_Field.last_edited, Sport_Field.geo_coordinate, "
                        +"Sport_Field.is_bike_parking, Sport_Field.is_car_parking, Sport_Field.is_public, "
                        +"Sport_Field.description, Sport_Field.rules, Sport_Field.time_open, Sport_Field.time_closed, "
                        +"Sport_Field.price_per_hour FROM Sport_Field INNER JOIN Sport_Kind ON "
                        +"(Sport_Field.Sport_Kind_id = Sport_Kind.id) ")
            if len(query_condition) > 6:
                query = query + query_condition

            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            read_row = cursor.fetchall()
            datas = []
            if body['coordinate'] != None:
                for i in range(cursor.rowcount):
                    data = {
                        "id": read_row[i]['id'],
                        "Sport_Kind_Name": read_row[i]['Sport_Kind_Name'],
                        "name": read_row[i]['name'],
                        "geo_coordinate": str(read_row[i]['geo_coordinate']),
                        "distance": calculateDistance(body['coordinate'], str(read_row[i]['geo_coordinate'])),
                        "is_bike_parking": read_row[i]['is_bike_parking'],
                        "is_car_parking": read_row[i]["is_car_parking"],
                        "is_public": read_row[i]['is_public'],
                        "price_per_hour": read_row[i]['price_per_hour']
                    }
                    datas = datas + [data]
            else:
                for i in range(cursor.rowcount):
                    data = {
                        "id": read_row[i]['id'],
                        "Sport_Kind_Name": read_row[i]['Sport_Kind_Name'],
                        "name": read_row[i]['name'],
                        "geo_coordinate": str(read_row[i]['geo_coordinate']),
                        "distance": None,
                        "is_bike_parking": read_row[i]['is_bike_parking'],
                        "is_car_parking": read_row[i]["is_car_parking"],
                        "is_public": read_row[i]['is_public'],
                        "price_per_hour": read_row[i]['price_per_hour']
                    }
                    datas = datas + [data]
            if body['sort_by'] == 'distance' and body['coordinate'] != None:
                datas = sorted(datas, key=lambda x: x['distance'])
            elif body['sort_by'] == 'price':
                datas = sorted(datas, key=lambda x: x['price_per_hour'])

            response = {
                "get_status": True,
                "message": "Retrieve Venues Successfully",
                "data": datas
            }
            code = 200
        else:
            response = {
                "get_status": False,
                "message": "Token is expired",
                "data": None
            }
            code = 401
        return jsonify(response)

    @app.route('/player/sportVenue/fields/<Sport_Venue_id>', methods=['GET'])
    def player_get_fields_from_venue(Sport_Venue_id):
        header = request.headers
        token = header['token']
        venue_id = Sport_Venue_id

        if checkPlayerToken(token):
            if isSportVenueExist(venue_id):
                query = "SELECT id, Sport_Field_id, number FROM Fields WHERE Sport_Field_id = '"+venue_id+"'"
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute(query)
                read_row = cursor.fetchall()

                response = {
                    "get_status": True,
                    "message": "Retrieve data fields from venue "+venue_id+" successfully",
                    "data": read_row
                }
                code = 200
                cursor.close()
                conn.close()
            else:
                response = {
                    "get_status": False,
                    "message": "There is no Venue with id "+ venue_id,
                    "data": None
                }
                code = 404
        else:
            response = {
                "get_status": False,
                "message": "Token is expired",
                "data": None
            }
            code = 401

        return jsonify(response), code

    @app.route('/player/sportVenue/fields/schedule/blacklist/<field_id>/<month>/<year>', methods=['GET'])
    def player_get_blacklist_schedule_from_month_and_year(field_id, month, year):
        header = request.headers
        token = header['token']
        field_id = field_id
        month = int(month)
        year = int(year)

        if checkPlayerToken(token):
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
                response = {
                    "get_status": True,
                    "message": "get blacklist schedule on this field is successfully",
                    "data": data
                }
                code = 200
                cursor.close()
                conn.close()
        else:
            response = {
                "get_status": False,
                "message": "token is expired",
                "data": None
            }
            code = 401
        return jsonify(response), code

    @app.route('/player/sportVenue/fields/schedule/reservation/<field_id>/<month>/<year>', methods=['GET'])
    def player_get_fields_reservation_in_a_month_and_year(field_id, month, year):
        token = request.headers['token']
        if checkPlayerToken(token):
            query = f"SELECT id, Field_id, Player_username, name, mabar_type, date, time_start, time_end, booking_status, payment_credential_url, is_public, is_open_member FROM Reservation WHERE Field_id = '{field_id}' AND MONTH(date)={month} AND YEAR(date)={year} AND booking_status NOT IN('cancelled', 'rejected')"
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
                    'id': results[i]['id'],
                    'Field_id': results[i]['Field_id'],
                    'Player_username': results[i]['Player_username'],
                    'name': results[i]['name'],
                    'mabar_type': results[i]['mabar_type'],
                    'date': results[i]['date'],
                    'time_start': str(results[i]['time_start']),
                    'time_end': str(results[i]['time_end']),
                    'booking_status': results[i]['booking_status'],
                    'payment_credential_url': results[i]['payment_credential_url'],
                    'is_public': results[i]['is_public'],
                    'is_open_member': results[i]['is_open_member']
                }
                datas = datas + [item]
            response = {
                'get_status': True,
                'message': f"Retrieve data reservation from field_id={field_id} in month={month} and year={year} successfully",
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

    @app.route('/player/sportVenue/<venue_id>', methods=['POST'])
    def player_get_venue_info_by_id(venue_id):
        token = request.headers['token']
        body = request.json
        if checkPlayerToken(token):
            if isSportVenueExist(venue_id):
                if isVenuePublic(venue_id):
                    query = ("SELECT Sport_Field.id, Sport_Field.Sport_Kind_id, Sport_Kind.name Sport_Kind_Name, Sport_Field.name, "
                        +"Sport_Field.created_at, Sport_Field.last_edited, Sport_Field.geo_coordinate, "
                        +"Sport_Field.is_bike_parking, Sport_Field.is_car_parking, Sport_Field.is_public, "
                        +"Sport_Field.description, Sport_Field.rules, Sport_Field.time_open, Sport_Field.time_closed, "
                        +"Sport_Field.price_per_hour FROM Sport_Field INNER JOIN Sport_Kind ON "
                        +f"(Sport_Field.Sport_Kind_id = Sport_Kind.id) WHERE Sport_Field.id = '{venue_id}'")

                    conn = mysql.connect()
                    cursor = conn.cursor(pymysql.cursors.DictCursor)
                    cursor.execute(query)
                    read_row = cursor.fetchone()
                    data = {
                        "id": read_row['id'],
                        "Sport_Kind_id": read_row['Sport_Kind_id'],
                        "Sport_Kind_Name": read_row['Sport_Kind_Name'],
                        "name": read_row['name'],
                        "created_at": str(read_row['created_at']),
                        "last_edited": str(read_row['last_edited']),
                        "geo_coordinate": str(read_row['geo_coordinate']),
                        "distance": calculateDistance(body['coordinate'], str(read_row['geo_coordinate'])),
                        "is_bike_parking": read_row['is_bike_parking'],
                        "is_car_parking": read_row["is_car_parking"],
                        "is_public": read_row['is_public'],
                        "description": read_row['description'],
                        "rules": read_row['rules'],
                        "time_open": str(read_row['time_open']),
                        "time_closed": str(read_row['time_closed']),
                        "price_per_hour": read_row['price_per_hour']
                    }
                    code = 200
                    response = {
                        'get_status': True,
                        'message': 'Retrieve venue info successfully',
                        'data': data
                    }
                else:
                    response = {
                        'get_status': False,
                        'message': f"Venue {venue_id} is not public",
                        'data': None
                    }
                    code = 403
            else:
                response = {
                    'get_status': False,
                    'message': f"Venue {venue_id} is not found",
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
