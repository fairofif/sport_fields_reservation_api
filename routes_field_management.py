import pymysql
from flask import (
    jsonify,
    request
)
from db_config import mysql
from dotenv import load_dotenv
from uuid_generator import newSportFieldUUID, newFieldUUID, newBlacklistScheduleUUID
import datetime
import calendar
load_dotenv(override=True)

def field_management_configure_routes(app):
    ### ================ STATIC METHOD ==================== ###
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

    def isFieldNumberExistInVenue(venue_id, field_number):
        query = "SELECT * FROM Fields WHERE Sport_Field_id = '"+venue_id+"' AND number = "+ str(field_number)

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

    def isUserOwnThisVenue(venue_id, username):
        query = f"SELECT id FROM Sport_Field WHERE id = '{venue_id}' and Admin_username = '{username}'"
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

    def get_day_of_week(date_string):
        date_object = datetime.datetime.strptime(date_string, "%Y-%m-%d")
        day_of_week = date_object.strftime("%A")
        return day_of_week

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

    def findUsernameFromToken(token):
        query = f"SELECT Admin_username FROM Admin_Login_Token WHERE token = '{token}'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data['Admin_username']

    def adminHasVenue(username):
        query = "SELECT * FROM Sport_Field WHERE Admin_username = '"+username+"'"
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

    def itIsAdminVenue(username, venue_id):
        query = f"SELECT id FROM Sport_Field WHERE id = '{venue_id}' AND Admin_username = '{username}'"
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

    ### ================ ROUTES ==================== ###

    @app.route('/sport_kinds', methods=['GET'])
    def get_sport_kind():
        query = "SELECT id, name FROM Sport_Kind"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        read_row = cursor.fetchall()
        cursor.close()
        conn.close()
        response = {
            "status_get": True,
            "message": "Retrieve sport kinds successfully",
            "data": read_row
        }
        code = 200

        return jsonify(response), code

    @app.route('/admin/sportVenue', methods=['GET'])
    def get_sport_venue():
        header = request.headers
        token = header['token']

        if checkAdminToken(token):
            admin_username = findUsernameFromToken(token)
            if (adminHasVenue(admin_username)):
                query = ("SELECT Sport_Field.id, Sport_Field.Sport_Kind_id, Sport_Kind.name Sport_Kind_Name, Sport_Field.name, "
                        +"Sport_Field.created_at, Sport_Field.last_edited, Sport_Field.geo_coordinate, "
                        +"Sport_Field.is_bike_parking, Sport_Field.is_car_parking, Sport_Field.is_public, "
                        +"Sport_Field.description, Sport_Field.rules, Sport_Field.time_open, Sport_Field.time_closed, "
                        +"Sport_Field.price_per_hour FROM Sport_Field INNER JOIN Sport_Kind ON "
                        +"(Sport_Field.Sport_Kind_id = Sport_Kind.id) WHERE Sport_Field.Admin_username = '"+admin_username+"'")
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute(query)
                read_row = cursor.fetchall()
                datas = []
                for i in range(cursor.rowcount):
                    data = {
                        "id": read_row[i]['id'],
                        "Sport_Kind_Name": read_row[i]['Sport_Kind_Name'],
                        "name": read_row[i]['name'],
                        "is_public": read_row[i]['is_public'],
                        "price_per_hour": read_row[i]['price_per_hour']
                    }
                    datas = datas = [data]
                response = {
                    "get_status": True,
                    "message": "Retrieve Sport Venue Successfully",
                    "data": datas
                }
                code = 200
                cursor.close()
                conn.close()
            else:
                response = {
                    "get_status": False,
                    "message": "Admin Has Not Registered any Venue",
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

    @app.route('/admin/sportVenue/register', methods=['POST'])
    def register_sport_venue():
        header = request.headers
        data = request.json
        token = header['token']
        Sport_Kind_id = data['Sport_Kind_id']
        name = data['name']
        geo_coordinate = data['geo_coordinate']
        is_bike_parking = data['is_bike_parking']
        is_car_parking = data['is_car_parking']
        is_public = data['is_public']
        description = data['description']
        rules = data['rules']
        time_open = data['time_open']
        time_closed = data['time_closed']
        price_per_hour = data['price_per_hour']

        if checkAdminToken(token):
            username = findUsernameFromToken(token)
            new_id_venue = newSportFieldUUID()
            query = ("INSERT INTO Sport_Field (id, Admin_username, Sport_Kind_id, name, created_at, last_edited, geo_coordinate"
                    + ", is_bike_parking, is_car_parking, is_public, description, rules, time_open, time_closed, price_per_hour)"
                    + " VALUES ('"+new_id_venue+"', '"+username+"', '"+Sport_Kind_id+"', '"+name+"', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), '"+geo_coordinate+"', "
                    + str(is_bike_parking)+", "+str(is_car_parking)+", "+str(is_public)+", '"+description+"', '"+rules+"', '"+time_open
                    + "', '"+time_closed+"', "+ str(price_per_hour)+")"
                    )
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            conn.commit()

            query = ("SELECT Sport_Field.id, Sport_Field.Sport_Kind_id, Sport_Kind.name Sport_Kind_Name, Sport_Field.name, "
                    +"Sport_Field.created_at, Sport_Field.last_edited, Sport_Field.geo_coordinate, "
                    +"Sport_Field.is_bike_parking, Sport_Field.is_car_parking, Sport_Field.is_public, "
                    +"Sport_Field.description, Sport_Field.rules, Sport_Field.time_open, Sport_Field.time_closed, "
                    +"Sport_Field.price_per_hour FROM Sport_Field INNER JOIN Sport_Kind ON "
                    +"(Sport_Field.Sport_Kind_id = Sport_Kind.id) WHERE Sport_Field.id = '"+new_id_venue+"'")

            cursor.execute(query)
            read_row = cursor.fetchone()
            cursor.close()
            conn.close()

            response = {
                "status_register": True,
                "message": "Register sport venue successfully",
                "data": {
                    "id": read_row['id'],
                    "Sport_Kind_id": read_row['Sport_Kind_id'],
                    "Sport_Kind_Name": read_row['Sport_Kind_Name'],
                    "name": read_row['name'],
                    "created_at": str(read_row['created_at']),
                    "last_edited": str(read_row['last_edited']),
                    "geo_coordinate": str(read_row['geo_coordinate']),
                    "is_bike_parking": read_row['is_bike_parking'],
                    "is_car_parking": read_row["is_car_parking"],
                    "is_public": read_row['is_public'],
                    "description": read_row['description'],
                    "rules": read_row['rules'],
                    "time_open": str(read_row['time_open']),
                    "time_closed": str(read_row['time_closed']),
                    "price_per_hour": read_row['price_per_hour']
                }
            }
            code = 200
        else:
            response = {
                "status_register": False,
                "message": "Token is expired",
                "data": None
            }
            code = 401

        return jsonify(response), code

    @app.route('/admin/sportVenue/edit', methods=['PUT'])
    def edit_sport_venue():
        header = request.headers
        data = request.json

        if checkAdminToken(header['token']):
            columns = [
                "Sport_Kind_id",
                "name",
                "geo_coordinate",
                "is_bike_parking",
                "is_car_parking",
                "is_public",
                "description",
                "rules",
                "time_open",
                "time_closed",
                "price_per_hour"
            ]

            query = "UPDATE Sport_Field SET "
            for i in range(len(columns)):
                if data[columns[i]] != None and type(data[columns[i]]) != bool:
                    query = query + columns[i] + " = '" + str(data[columns[i]]) + "', "
                elif data[columns[i]] != None and type(data[columns[i]]) == bool:
                    query = query + columns[i] + " = '" + str(int(data[columns[i]])) + "', "

            query = query + "last_edited = CURRENT_TIMESTAMP() "
            query = query + "WHERE id = '" + data['id'] + "'"

            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            conn.commit()

            query = ("SELECT Sport_Field.id, Sport_Field.Sport_Kind_id, Sport_Kind.name Sport_Kind_Name, Sport_Field.name, "
                    +"Sport_Field.created_at, Sport_Field.last_edited, Sport_Field.geo_coordinate, "
                    +"Sport_Field.is_bike_parking, Sport_Field.is_car_parking, Sport_Field.is_public, "
                    +"Sport_Field.description, Sport_Field.rules, Sport_Field.time_open, Sport_Field.time_closed, "
                    +"Sport_Field.price_per_hour FROM Sport_Field INNER JOIN Sport_Kind ON "
                    +"(Sport_Field.Sport_Kind_id = Sport_Kind.id) WHERE Sport_Field.id = '"+data['id']+"'")
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            read_row = cursor.fetchone()

            response = {
                "update_status": True,
                "message": "Edit venue successfully",
                "data": {
                    "id": read_row['id'],
                    "Sport_Kind_id": read_row['Sport_Kind_id'],
                    "Sport_Kind_Name": read_row['Sport_Kind_Name'],
                    "name": read_row['name'],
                    "created_at": str(read_row['created_at']),
                    "last_edited": str(read_row['last_edited']),
                    "geo_coordinate": str(read_row['geo_coordinate']),
                    "is_bike_parking": read_row['is_bike_parking'],
                    "is_car_parking": read_row["is_car_parking"],
                    "is_public": read_row['is_public'],
                    "description": read_row['description'],
                    "rules": read_row['rules'],
                    "time_open": str(read_row['time_open']),
                    "time_closed": str(read_row['time_closed']),
                    "price_per_hour": read_row['price_per_hour']
                }
            }
            code = 200
        else:
            query = ("SELECT Sport_Field.id, Sport_Field.Sport_Kind_id, Sport_Kind.name Sport_Kind_Name, Sport_Field.name, "
                    +"Sport_Field.created_at, Sport_Field.last_edited, Sport_Field.geo_coordinate, "
                    +"Sport_Field.is_bike_parking, Sport_Field.is_car_parking, Sport_Field.is_public, "
                    +"Sport_Field.description, Sport_Field.rules, Sport_Field.time_open, Sport_Field.time_closed, "
                    +"Sport_Field.price_per_hour FROM Sport_Field INNER JOIN Sport_Kind ON "
                    +"(Sport_Field.Sport_Kind_id = Sport_Kind.id) WHERE Sport_Field.id = '"+data['id']+"'")
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            read_row = cursor.fetchone()
            response = {
                "update_status": False,
                "message": "Token is expired, update failed",
                "data": {
                    "id": read_row['id'],
                    "Sport_Kind_id": read_row['Sport_Kind_id'],
                    "Sport_Kind_Name": read_row['Sport_Kind_Name'],
                    "name": read_row['name'],
                    "created_at": str(read_row['created_at']),
                    "last_edited": str(read_row['last_edited']),
                    "geo_coordinate": str(read_row['geo_coordinate']),
                    "is_bike_parking": read_row['is_bike_parking'],
                    "is_car_parking": read_row["is_car_parking"],
                    "is_public": read_row['is_public'],
                    "description": read_row['description'],
                    "rules": read_row['rules'],
                    "time_open": str(read_row['time_open']),
                    "time_closed": str(read_row['time_closed']),
                    "price_per_hour": read_row['price_per_hour']
                }
            }
            code = 401
        cursor.close()
        conn.close()

        return jsonify(response)

    @app.route('/admin/sportVenue/fields/add', methods=['POST'])
    def add_field_to_venue():
        token = request.headers['token']
        data = request.json
        venue_id = data['Sport_Venue_id']
        number = data['field_number']

        if checkAdminToken(token):
            if isFieldNumberExistInVenue(venue_id, number):
                query = "SELECT id, Sport_Field_id, number FROM Fields WHERE Sport_Field_id = '"+venue_id+"'"
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute(query)
                read_row = cursor.fetchall()

                response = {
                    "add_status": False,
                    "message": "Field Number already exist in this selected venue",
                    "data": read_row
                }
                code = 409
            else:
                query = "INSERT INTO Fields VALUES ('"+newFieldUUID()+"', '"+venue_id+"', "+str(number)+", CURRENT_TIMESTAMP())"
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute(query)
                conn.commit()

                query = "SELECT id, Sport_Field_id, number FROM Fields WHERE Sport_Field_id = '"+venue_id+"'"
                cursor.execute(query)
                read_row = cursor.fetchall()

                response = {
                    "add_status": True,
                    "message": "Field number "+str(number)+" has been added to venue "+venue_id+" successfully",
                    "data": read_row
                }
                code = 200
        else:
            query = "SELECT id, Sport_Field_id, number FROM Fields WHERE Sport_Field_id = '"+venue_id+"'"
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            read_row = cursor.fetchall()

            response = {
                "add_status": False,
                "message": "Token is expired",
                "data": read_row
            }
            code = 401
        cursor.close()
        conn.close()

        return jsonify(response), code

    @app.route('/admin/sportVenue/fields/delete', methods=['DELETE'])
    def delete_field_from_venue():
        token = request.headers['token']
        data = request.json
        field_id = data['field_id']
        venue_id = data['Sport_Venue_id']

        if checkAdminToken(token):
            query = "DELETE FROM Fields WHERE id = '"+field_id+"'"
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            conn.commit()

            query = "SELECT id, Sport_Field_id, number FROM Fields WHERE Sport_Field_id = '"+venue_id+"'"
            cursor.execute(query)
            read_row = cursor.fetchall()

            response = {
                "delete_status": True,
                "message": "Field with id "+field_id+" has been removed successfully",
                "data": read_row
            }
            code = 200

            cursor.close()
            conn.close()

        else:
            response = {
                "delete_status": False,
                "message": "Token is expired",
                "data": None
            }
            code = 401

        return jsonify(response), code

    @app.route('/admin/sportVenue/fields/<Sport_Venue_id>', methods=['GET'])
    def get_fields_from_venue(Sport_Venue_id):
        header = request.headers
        token = header['token']
        venue_id = Sport_Venue_id

        if checkAdminToken(token):
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

    @app.route('/admin/sportVenue/fields/schedule/blacklist', methods=['POST'])
    def add_blacklist_schedule():
        header = request.headers
        token = header['token']
        data = request.json
        field_id = data['Field_id']
        date = data['date']
        from_time = data['fromTime']
        to_time = data['toTime']
        is_every_week = data['is_every_week']
        reason = data['reason']

        if checkAdminToken(token):
            query = f"INSERT INTO Blacklist_Schedule Values('{newBlacklistScheduleUUID()}', '{field_id}', '{date}', '{from_time}', '{to_time}', '{int(is_every_week)}', '{reason}', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP())"
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            conn.commit()
            cursor.close()
            conn.close()

            if is_every_week == False:
                response = {
                    "blacklist_status": True,
                    "message": f"Schedule on {date} is already in blacklist schedule"
                }
                code = 200
            else:
                response = {
                    "blacklist_status": True,
                    "message": f"Every {get_day_of_week(date)} from {from_time} to {to_time} is in blacklist schedule"
                }
                code = 200
        else:
            response = {
                "blacklist_status": False,
                "message": "Token is expired"
            }
            code = 401

        return jsonify(response)

    @app.route('/admin/sportVenue/fields/schedule/blacklist/<field_id>/<month>/<year>', methods=['GET'])
    def get_blacklist_schedule_from_month_and_year(field_id, month, year):
        header = request.headers
        token = header['token']
        field_id = field_id
        month = int(month)
        year = int(year)

        if checkAdminToken(token):
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

    @app.route('/admin/sportVenue/fields/schedule/blacklist', methods=['DELETE'])
    def delete_blacklist_schedule():
        header = request.headers
        body = request.json
        token = header['token']
        blacklist_id = body['blacklist_id']

        if checkAdminToken(token):
            query = f"DELETE FROM Blacklist_Schedule WHERE id = '{blacklist_id}'"
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            conn.commit()
            cursor.close()
            conn.close()

            response = {
                "delete_status": True,
                "message": f"Blacklist with id = {blacklist_id} deleted successfully",
                "data": {
                    "deleted_blacklist": {
                        "blacklist_id": blacklist_id
                    }
                }
            }
            code = 200
        else:
            response = {
                "deleted_status": False,
                "message": "Token is expired",
                "data": None
            }
            code = 401
        return jsonify(response), code

    @app.route('/admin/sportVenue/fields/schedule/reservation/<field_id>/<month>/<year>', methods=['GET'])
    def get_fields_reservation_in_a_month_and_year(field_id, month, year):
        token = request.headers['token']
        if checkAdminToken(token):
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

    @app.route('/admin/sportVenue/<venue_id>', methods=['GET'])
    def admin_get_sport_venue_by_id(venue_id):
        token = request.headers['token']
        if checkAdminToken(token):
            username = findUsernameFromToken(token)
            if isUserOwnThisVenue(venue_id, username):
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
                    'message': f"{venue_id} is not {username}'s venue",
                    'data': None
                }
                code = 403
        else:
            response = {
                'get_status': False,
                'message': 'Token is expired',
                'data': None
            }
            code = 401

        return jsonify(response), code

    @app.route('/admin/sportVenue/<venue_id>', methods=['DELETE'])
    def delete_venue_by_id(venue_id):
        token = request.headers['token']
        if checkAdminToken(token):
            if isSportVenueExist(venue_id):
                username = findUsernameFromToken(token)
                if itIsAdminVenue(username, venue_id):
                    query = f"DELETE FROM Sport_Field WHERE id = '{venue_id}'"
                    conn = mysql.connect()
                    cursor = conn.cursor(pymysql.cursors.DictCursor)
                    cursor.execute(query)
                    conn.commit()
                    cursor.close()
                    conn.close()
                    response = {
                        'delete_status': True,
                        'message': f"Venue {venue_id} has been deleted",
                        'data': {
                            'venue_id': venue_id
                        }
                    }
                    code = 200
                else:
                    response = {
                        'delete_status': False,
                        'message': f"{username} is not admin of Venue {venue_id}",
                        'data': None
                    }
                    code = 403

            else:
                response = {
                    'delete_status': False,
                    'message': f"Venue {venue_id} not found",
                    'data': None
                }
                code = 404
        else:
            response = {
                'delete_status': False,
                'message': 'Token is expired',
                'data': None
            }
            code = 401

        return jsonify(response), code



