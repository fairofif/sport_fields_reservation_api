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
                        "Sport_Kind_id": read_row[i]['Sport_Kind_id'],
                        "Sport_Kind_Name": read_row[i]['Sport_Kind_Name'],
                        "name": read_row[i]['name'],
                        "created_at": str(read_row[i]['created_at']),
                        "last_edited": str(read_row[i]['last_edited']),
                        "geo_coordinate": str(read_row[i]['geo_coordinate']),
                        "distance": calculateDistance(body['coordinate'], str(read_row[i]['geo_coordinate'])),
                        "is_bike_parking": read_row[i]['is_bike_parking'],
                        "is_car_parking": read_row[i]["is_car_parking"],
                        "is_public": read_row[i]['is_public'],
                        "description": read_row[i]['description'],
                        "rules": read_row[i]['rules'],
                        "time_open": str(read_row[i]['time_open']),
                        "time_closed": str(read_row[i]['time_closed']),
                        "price_per_hour": read_row[i]['price_per_hour']
                    }
                    datas = datas + [data]
            else:
                for i in range(cursor.rowcount):
                    data = {
                        "id": read_row[i]['id'],
                        "Sport_Kind_id": read_row[i]['Sport_Kind_id'],
                        "Sport_Kind_Name": read_row[i]['Sport_Kind_Name'],
                        "name": read_row[i]['name'],
                        "created_at": str(read_row[i]['created_at']),
                        "last_edited": str(read_row[i]['last_edited']),
                        "geo_coordinate": str(read_row[i]['geo_coordinate']),
                        "distance": None,
                        "is_bike_parking": read_row[i]['is_bike_parking'],
                        "is_car_parking": read_row[i]["is_car_parking"],
                        "is_public": read_row[i]['is_public'],
                        "description": read_row[i]['description'],
                        "rules": read_row[i]['rules'],
                        "time_open": str(read_row[i]['time_open']),
                        "time_closed": str(read_row[i]['time_closed']),
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
        else:
            response = {
                "get_status": False,
                "message": "Token is expired",
                "data": None
            }
        return jsonify(response)