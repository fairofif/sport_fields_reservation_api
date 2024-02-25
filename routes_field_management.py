import pymysql
from flask import (
    jsonify,
    request
)
from db_config import mysql
from dotenv import load_dotenv
from uuid_generator import newSportFieldUUID
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

    @app.route('/admin/sportVenue/register', methods=['POST'])
    def register_sport_venue():
        header = request.headers
        data = request.json
        token = header['token']
        username = data['username']
        sport_kind_uuid = data['sport_kind_uuid']
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
                    + " VALUES ('"+newSportFieldUUID()+"', '"+username+"', '"+sport_kind_uuid+"', '"+name+"', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), '"+geo_coordinate+"', "
                    + str(is_bike_parking)+", "+str(is_car_parking)+", "+str(is_public)+", '"+description+"', '"+rules+"', '"+time_open
                    + "', '"+time_closed+"', "+ str(price_per_hour)+")"
                    )
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            conn.commit()
            cursor.close()
            conn.close()
            response = {
                "status_register": True,
                "message": "Register sport venue successfully",
            }
        else:
            response = {
                "status_register": False,
                "message": "Token is expired"
            }

        return jsonify(response)