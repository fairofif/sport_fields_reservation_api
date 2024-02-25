from db_config import mysql
import pymysql
from app import app
from dotenv import load_dotenv
load_dotenv()
import os
from token_generator import newAdminToken
from virtual_device_id_generator import newVirtualDeviceID
from uuid_generator import newSportKindUUID

def insert_unittest_user():
    ava_url = os.getenv("DEFAULT_AVA_PATH")

    query = 'INSERT INTO Admin VALUES("unittest", "Unit Test", "unittest", "unittest", "'+ava_url+'", CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP())'
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def delete_unittest_user():
    query = 'DELETE FROM Admin WHERE username = "unittest"'
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def delete_unittest_token(token):
    query = "DELETE FROM Admin_Login_Token WHERE token = '"+token+"'"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def insert_unittest_token(token, device_id):
    query = "INSERT INTO Admin_Login_Token VALUES ('"+token+"', 'unittest', CURRENT_TIMESTAMP(), '"+device_id+"')"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def insert_unittest_device(device_id):
    query = "INSERT INTO Virtual_Device_ID VALUES ('"+device_id+"', CURRENT_TIMESTAMP())"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def delete_unittest_device(device_id):
    query = "DELETE FROM Virtual_Device_ID WHERE id = '"+device_id+"'"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def insert_unittest_sport_kind():
    uuid = newSportKindUUID()
    query = "INSERT INTO Sport_Kind (id, name) VALUES ('"+uuid+"', 'unittest_sport')"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
    return uuid

def delete_unittest_sport_kind(uuid):
    query = "DELETE FROM Sport_Kind WHERE id = '"+uuid+"'"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

### =========================== UNIT TEST =========================== ###

def test_get_all_sport_kind():
    sport_kind_uuid = insert_unittest_sport_kind()

    client = app.test_client()
    url = "/sport_kinds"

    response = client.get(url)

    delete_unittest_sport_kind(sport_kind_uuid)

    assert response.status_code == 200

def test_register_sport_venue():
    device = newVirtualDeviceID()
    token = newAdminToken()
    sport_kind_uuid = insert_unittest_sport_kind()

    insert_unittest_user()
    insert_unittest_device(device)
    insert_unittest_token(token, device)

    client = app.test_client()
    url = "/admin/sportVenue/register"

    header = {
        "token": token
    }

    body_request = {
        "username": "unittest",
        "sport_kind_uuid": sport_kind_uuid,
        "name": "Unit Test Venue",
        "geo_coordinate": "-6.300012, 107.164228",
        "is_bike_parking": True,
        "is_car_parking": True,
        "is_public": False,
        "description": "Unit Test Venue Description",
        "rules": "Unit Test Venue Rules",
        "time_open": "08:00:00",
        "time_closed": "23:00:00",
        "price_per_hour": 40000
    }

    response = client.post(url, json=body_request, headers=header)

    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind_uuid)
    delete_unittest_device(device)

    assert response.status_code == 200
    assert response.get_json()['status_register'] == True
