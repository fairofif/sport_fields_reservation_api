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
load_dotenv()

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

        return jsonify(response)

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
                        "Sport_Kind_id": read_row[i]['Sport_Kind_id'],
                        "Sport_Kind_Name": read_row[i]['Sport_Kind_Name'],
                        "name": read_row[i]['name'],
                        "created_at": str(read_row[i]['created_at']),
                        "last_edited": str(read_row[i]['last_edited']),
                        "geo_coordinate": str(read_row[i]['geo_coordinate']),
                        "is_bike_parking": read_row[i]['is_bike_parking'],
                        "is_car_parking": read_row[i]["is_car_parking"],
                        "is_public": read_row[i]['is_public'],
                        "description": read_row[i]['description'],
                        "rules": read_row[i]['rules'],
                        "time_open": str(read_row[i]['time_open']),
                        "time_closed": str(read_row[i]['time_closed']),
                        "price_per_hour": read_row[i]['price_per_hour']
                    }
                response = {
                    "get_status": True,
                    "message": "Retrieve Sport Venue Successfully",
                    "data": datas
                }
                cursor.close()
                conn.close()
            else:
                response = {
                    "get_status": False,
                    "message": "Admin Has Not Registered any Venue",
                    "data": None
                }
        else:
            response = {
                "get_status": False,
                "message": "Token is expired",
                "data": None
            }

        return jsonify(response)

    @app.route('/admin/sportVenue/register', methods=['POST'])
    def register_sport_venue():
        header = request.headers
        data = request.json
        token = header['token']
        username = data['username']
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
        else:
            response = {
                "status_register": False,
                "message": "Token is expired",
                "data": None
            }

        return jsonify(response)

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
        cursor.close()
        conn.close()

        return jsonify(response)

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

            cursor.close()
            conn.close()

        else:
            response = {
                "delete_status": False,
                "message": "Token is expired",
                "data": None
            }

        return jsonify(response)

    @app.route('/admin/sportVenue/fields', methods=['GET'])
    def get_fields_from_venue():
        header = request.headers
        token = header['token']
        venue_id = header['Sport-Venue-id']

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
                cursor.close()
                conn.close()
            else:
                response = {
                    "get_status": False,
                    "message": "There is no Venue with id "+ venue_id,
                    "data": None
                }
        else:
            response = {
                "get_status": False,
                "message": "Token is expired",
                "data": None
            }

        return jsonify(response)

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
            else:
                response = {
                    "blacklist_status": True,
                    "message": f"Every {get_day_of_week(date)} from {from_time} to {to_time} is in blacklist schedule"
                }
        else:
            response = {
                "blacklist_status": False,
                "message": "Token is expired"
            }

        return jsonify(response)

    @app.route('/admin/sportVenue/fields/schedule/blacklist', methods=['GET'])
    def get_blacklist_schedule_from_month_and_year():
        header = request.headers
        token = header['token']
        field_id = header['field_id']
        month = int(header['month'])
        year = int(header['year'])

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
                                print(i, j)
                                if date_in_a_month[j].day >= format_date.day and date_in_a_month[j].strftime("%A") == day_date:
                                    item = {
                                        "blacklist_id": str(query_resp[i]['blacklist_id']),
                                        "date": str(date_in_a_month[j].strftime('%Y-%m-%d')),
                                        "fromTime": str(query_resp[i]['fromTime']),
                                        "toTime": str(query_resp[i]['toTime']),
                                        "reason": str(query_resp[i]['reason'])
                                        }
                                    print(1, item)
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
                cursor.close()
                conn.close()
        else:
            response = {
                "get_status": False,
                "message": "token is expired",
                "data": None
            }
        return jsonify(response)

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
                "data": None
            }
        else:
            response = {
                "deleted_status": False,
                "message": "Token is expired",
                "data": None
            }
        return jsonify(response)
