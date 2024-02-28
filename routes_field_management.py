import pymysql
from flask import (
    jsonify,
    request
)
from db_config import mysql
from dotenv import load_dotenv
from uuid_generator import newSportFieldUUID, newFieldUUID
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
        venue_id = header['Sport_Venue_id']

        if checkAdminToken(token):
            if isSportVenueExist(venue_id):
                query = ("SELECT Sport_Field.id, Sport_Field.Sport_Kind_id, Sport_Kind.name Sport_Kind_Name, Sport_Field.name, "
                        +"Sport_Field.created_at, Sport_Field.last_edited, Sport_Field.geo_coordinate, "
                        +"Sport_Field.is_bike_parking, Sport_Field.is_car_parking, Sport_Field.is_public, "
                        +"Sport_Field.description, Sport_Field.rules, Sport_Field.time_open, Sport_Field.time_closed, "
                        +"Sport_Field.price_per_hour FROM Sport_Field INNER JOIN Sport_Kind ON "
                        +"(Sport_Field.Sport_Kind_id = Sport_Kind.id) WHERE Sport_Field.id = '"+venue_id+"'")
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute(query)
                read_row = cursor.fetchone()

                response = {
                    "get_status": True,
                    "message": "Retrieve Sport Venue Successfully",
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
            else:
                response = {
                    "get_status": False,
                    "message": "Venue id "+venue_id+" is not registered yet",
                    "data": {
                        "id": None,
                        "Sport_Kind_id": None,
                        "Sport_Kind_Name": None,
                        "name": None,
                        "created_at": None,
                        "last_edited": None,
                        "geo_coordinate": None,
                        "is_bike_parking": None,
                        "is_car_parking": None,
                        "is_public": None,
                        "description": None,
                        "rules": None,
                        "time_open": None,
                        "time_closed": None,
                        "price_per_hour": None
                    }
                }
        else:
            response = {
                "get_status": False,
                "message": "Token is expired",
                "data": {
                    "id": None,
                    "Sport_Kind_id": None,
                    "Sport_Kind_Name": None,
                    "name": None,
                    "created_at": None,
                    "last_edited": None,
                    "geo_coordinate": None,
                    "is_bike_parking": None,
                    "is_car_parking": None,
                    "is_public": None,
                    "description": None,
                    "rules": None,
                    "time_open": None,
                    "time_closed": None,
                    "price_per_hour": None
                }
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
            query = ("INSERT INTO Sport_Field (id, Admin_username, Sport_Kind_id, name, created_at, last_edited, geo_coordinate"
                    + ", is_bike_parking, is_car_parking, is_public, description, rules, time_open, time_closed, price_per_hour)"
                    + " VALUES ('"+newSportFieldUUID()+"', '"+username+"', '"+Sport_Kind_id+"', '"+name+"', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), '"+geo_coordinate+"', "
                    + str(is_bike_parking)+", "+str(is_car_parking)+", "+str(is_public)+", '"+description+"', '"+rules+"', '"+time_open
                    + "', '"+time_closed+"', "+ str(price_per_hour)+")"
                    )
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            conn.commit()

            query = "SELECT id, Admin_username FROM Sport_Field WHERE Admin_username = '"+username+"'"
            cursor.execute(query)
            read_row = cursor.fetchone()

            query = ("SELECT Sport_Field.id, Sport_Field.Sport_Kind_id, Sport_Kind.name Sport_Kind_Name, Sport_Field.name, "
                    +"Sport_Field.created_at, Sport_Field.last_edited, Sport_Field.geo_coordinate, "
                    +"Sport_Field.is_bike_parking, Sport_Field.is_car_parking, Sport_Field.is_public, "
                    +"Sport_Field.description, Sport_Field.rules, Sport_Field.time_open, Sport_Field.time_closed, "
                    +"Sport_Field.price_per_hour FROM Sport_Field INNER JOIN Sport_Kind ON "
                    +"(Sport_Field.Sport_Kind_id = Sport_Kind.id) WHERE Sport_Field.id = '"+read_row['id']+"'")

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
                "data": {
                    "id": None,
                    "Sport_Kind_id": None,
                    "Sport_Kind_Name": None,
                    "name": None,
                    "created_at": None,
                    "last_edited": None,
                    "geo_coordinate": None,
                    "is_bike_parking": None,
                    "is_car_parking": None,
                    "is_public": None,
                    "description": None,
                    "rules": None,
                    "time_open": None,
                    "time_closed": None,
                    "price_per_hour": None
                }
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

                print(query)
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
