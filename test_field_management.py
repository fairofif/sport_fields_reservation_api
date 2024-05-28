from db_config import mysql
import pymysql
from app import app
from dotenv import load_dotenv
load_dotenv()
import os
from token_generator import newUserToken
from virtual_device_id_generator import newVirtualDeviceID
from uuid_generator import newSportKindUUID, newSportFieldUUID, newFieldUUID, newBlacklistScheduleUUID, newBookingUUID
from static import insert_album_photo, soft_delete_photo_album
import pytest

def insert_unittest_user():
    ava_url = os.getenv("DEFAULT_AVA_PATH")

    query = 'INSERT INTO Admin VALUES("unittest", "Unit Test", "unittest", "unittest", "'+ava_url+'", CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP())'
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def insert_unittest_user_custom(username):
    ava_url = os.getenv("DEFAULT_AVA_PATH")

    query = 'INSERT INTO Admin VALUES("'+username+'", "Unit Test", "unittest", "unittest", "'+ava_url+'", CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP())'
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

def delete_unittest_user_custom(username):
    query = f"DELETE FROM Admin WHERE username = '{username}'"
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

def insert_unittest_token_custom(token, device_id, username):
    query = f"INSERT INTO Admin_Login_Token VALUES ('{token}', '{username}', CURRENT_TIMESTAMP(), '{device_id}')"
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

def insert_unittest_sport_venue(venue_id, sport_kind_id):
    query = "INSERT INTO Sport_Field VALUES ('"+venue_id+"', 'unittest', '"+sport_kind_id+"', 'unittest', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), '-6.300012, 107.164228', 1, 1, 0, 'unittest', 'unittest', '08:00:00', '23:00:00', 40000)"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def delete_unittest_sport_venue(venue_id):
    query = "DELETE FROM Sport_Field WHERE id = '"+venue_id+"'"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def insert_unittest_field_to_venue(field_id, venue_id, number):
    query = "INSERT INTO Fields VALUES ('"+field_id+"', '"+venue_id+"', "+str(number)+", CURRENT_TIMESTAMP())"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def delete_unittest_field_from_venue(field_id):
    query = "DELETE FROM Fields WHERE id = '"+field_id+"'"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def insert_unittest_blacklist_one_time_only(blacklist_id, field_id):
    query = f"INSERT INTO Blacklist_Schedule VALUES ('{blacklist_id}', '{field_id}', '2024-07-20', '08:00:00', '11:00:00', 0, 'Cuti Khusus', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP)"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def insert_unittest_blacklist_every_week(blacklist_id, field_id):
    query = f"INSERT INTO Blacklist_Schedule VALUES ('{blacklist_id}', '{field_id}', '2024-07-20', '08:00:00', '11:00:00', 1, 'Cuti Khusus', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP)"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def delete_unittest_delete_blacklist(blacklist_id):
    query = f"DELETE FROM Blacklist_Schedule WHERE id = '{blacklist_id}'"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

### ============= PLAYER REQUIREMENTS STATIC METHOD ================ ###
def insert_booking_unittest(book_id, field_id, date, time_start, time_end):
    query = "INSERT INTO Reservation (id, Field_id, Player_username, name, mabar_type, date, time_start, time_end, created_at, last_updated) VALUES "
    query = query + f"('{book_id}', '{field_id}', 'unittest', 'Mabar Orang Ganteng', 'friendly', '{date}', '{time_start}', '{time_end}', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP())"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def insert_player_unittest_user():
    ava_url = os.getenv("DEFAULT_AVA_PATH")

    query = 'INSERT INTO Player VALUES("unittest", "unittest", "Unit Test", "'+ava_url+'", CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), "08123456789")'
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def delete_player_unittest_user():
    query = 'DELETE FROM Player WHERE username = "unittest"'
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

### =========================== UNIT TEST =========================== ###

def test_get_all_sport_kind():
    """Test to get all of sport kind"""
    Sport_Kind_id = insert_unittest_sport_kind()

    client = app.test_client()
    url = "/sport_kinds"

    response = client.get(url)

    delete_unittest_sport_kind(Sport_Kind_id)

    assert response.status_code == 200

def test_get_sport_venue_success():
    """Test to get managed venue information by admin with valid request"""
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)

    client = app.test_client()
    url = "/admin/sportVenue"

    header = {
        "token": token
    }

    response = client.get(url, headers=header)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True

def test_get_sport_venue_failed():
    """test to get managed venue information by admin but with failed request"""
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)

    client = app.test_client()
    url = "/admin/sportVenue"

    header = {
        "token": token
    }

    response = client.get(url, headers=header)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)

    assert response.status_code == 404
    assert response.get_json()['get_status'] == False

def test_register_sport_venue():
    """Test to register managed venue by admin"""
    device = newVirtualDeviceID()
    token = newUserToken()
    Sport_Kind_id = insert_unittest_sport_kind()

    insert_unittest_user()
    insert_unittest_device(device)
    insert_unittest_token(token, device)

    client = app.test_client()
    url = "/admin/sportVenue/register"

    header = {
        "token": token
    }

    body_request = {
        "Sport_Kind_id": Sport_Kind_id,
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
    delete_unittest_sport_kind(Sport_Kind_id)
    delete_unittest_device(device)

    assert response.status_code == 200
    assert response.get_json()['status_register'] == True

def test_edit_sport_venue():
    """Test to edit managed sport venue by admin"""
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)

    client = app.test_client()
    url = '/admin/sportVenue/edit'

    header = {
        "token": token
    }

    body = {
        "id": sport_venue,
        "Sport_Kind_id": None,
        "name": "Edited Name Venue",
        "geo_coordinate": None,
        "is_bike_parking": None,
        "is_car_parking": None,
        "is_public": True,
        "description": None,
        "rules": None,
        "time_open": None,
        "time_closed": None,
        "price_per_hour": 40000
    }

    response = client.put(url, headers=header, json=body)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)

    assert response.status_code == 200
    assert response.get_json()['update_status'] == True

def test_add_fields_to_venue_success():
    """Test add fields to some venue that managed by admin and success response"""
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)

    client = app.test_client()
    url = '/admin/sportVenue/fields/add'

    header = {
        "token": token
    }

    body = {
        "Sport_Venue_id": sport_venue,
        "field_number": 1
    }

    response = client.post(url, headers=header, json=body)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)

    assert response.status_code == 200
    assert response.get_json()['add_status'] == True

def test_add_fields_to_venue_failed():
    """Test add fields to some venue that managed by admin but failed"""
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)

    field_id = newFieldUUID()
    insert_unittest_field_to_venue(field_id, sport_venue, 1)

    client = app.test_client()
    url = '/admin/sportVenue/fields/add'

    header = {
        "token": token
    }

    body = {
        "Sport_Venue_id": sport_venue,
        "field_number": 1
    }

    response = client.post(url, headers=header, json=body)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)

    assert response.status_code == 409
    assert response.get_json()['add_status'] == False

def test_get_fields_from_venue_success():
    """Test getting field list from managed venue by admin with valid request"""
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)

    field_id = newFieldUUID()
    insert_unittest_field_to_venue(field_id, sport_venue, 1)

    header = {
        "token": token,
    }

    client = app.test_client()
    url = f"/admin/sportVenue/fields/{sport_venue}"

    response = client.get(url, headers=header)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True

def test_get_fields_from_venue_failed():
    """Test getting field list from managed venue by admin with invalid request"""
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)

    field_id = newFieldUUID()
    insert_unittest_field_to_venue(field_id, sport_venue, 1)

    header = {
        "token": token
    }

    client = app.test_client()
    url = f"/admin/sportVenue/fields/{newSportFieldUUID()}"

    response = client.get(url, headers=header)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)

    assert response.status_code == 404
    assert response.get_json()['get_status'] == False

def test_delete_field_from_venue_success():
    """Test deleting a field from managed venue by admin with valid request"""
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)

    field_id = newFieldUUID()
    insert_unittest_field_to_venue(field_id, sport_venue, 1)

    header = {
        "token": token
    }

    body = {
        "field_id": field_id,
        "Sport_Venue_id": sport_venue
    }

    client = app.test_client()
    url = '/admin/sportVenue/fields/delete'

    response = client.delete(url, headers=header, json=body)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)

    assert response.status_code == 200
    assert response.get_json()['delete_status'] == True

def test_add_blacklist_schedule_from_a_field_success():
    """Test adding a blacklist schedule from a fields with valid request"""
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)

    field_id = newFieldUUID()
    insert_unittest_field_to_venue(field_id, sport_venue, 1)

    header = {
        "token": token
    }

    body = {
        "Field_id": field_id,
        "date": "2024-05-20",
        "fromTime": "08:00:00",
        "toTime": "10:59:59",
        "reason": "Cuti Perayaan",
        "is_every_week": False
    }

    client = app.test_client()
    url = '/admin/sportVenue/fields/schedule/blacklist'

    response = client.post(url, headers=header, json=body)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)

    assert response.status_code == 200
    assert response.get_json()['blacklist_status'] == True

def test_get_blacklist_schedule_one_time_only():
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)

    field_id = newFieldUUID()
    insert_unittest_field_to_venue(field_id, sport_venue, 1)

    blacklist_id = newBlacklistScheduleUUID()
    insert_unittest_blacklist_one_time_only(blacklist_id, field_id)

    header = {
        "token": token
    }

    param = {
        "field_id": field_id,
        "month": 7,
        "year": 2024
    }

    url = f"admin/sportVenue/fields/schedule/blacklist/{param['field_id']}/{str(param['month'])}/{str(param['year'])}"
    client = app.test_client()

    response = client.get(url, headers=header)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)

    assert response.status_code == 200
    assert response.get_json()['data'] != None

def test_get_blacklist_schedule_every_week():
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)

    field_id = newFieldUUID()
    insert_unittest_field_to_venue(field_id, sport_venue, 1)

    blacklist_id = newBlacklistScheduleUUID()
    insert_unittest_blacklist_every_week(blacklist_id, field_id)

    header = {
        "token": token
    }

    param = {
        "field_id": field_id,
        "month": 9,
        "year": 2024
    }

    url = f"admin/sportVenue/fields/schedule/blacklist/{param['field_id']}/{str(param['month'])}/{str(param['year'])}"
    client = app.test_client()
    response = client.get(url, headers=header)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)

    assert response.status_code == 200
    assert response.get_json()['data'] != None
    assert len(response.get_json()['data']) > 1

def test_get_blacklist_schedule_every_week_failed():
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)

    field_id = newFieldUUID()
    insert_unittest_field_to_venue(field_id, sport_venue, 1)

    blacklist_id = newBlacklistScheduleUUID()
    insert_unittest_blacklist_every_week(blacklist_id, field_id)

    header = {
        "token": token
    }

    param = {
        "field_id": field_id,
        "month": 5,
        "year": 2019
    }

    url = f"admin/sportVenue/fields/schedule/blacklist/{param['field_id']}/{str(param['month'])}/{str(param['year'])}"
    client = app.test_client()
    response = client.get(url, headers=header)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)

    assert response.status_code == 200
    assert len(response.get_json()['data']) == 0

def test_delete_blacklist_schedule():
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)

    field_id = newFieldUUID()
    insert_unittest_field_to_venue(field_id, sport_venue, 1)

    blacklist_id = newBlacklistScheduleUUID()
    insert_unittest_blacklist_every_week(blacklist_id, field_id)

    header = {
        "token": token
    }

    body = {
        "blacklist_id": blacklist_id
    }

    url = 'admin/sportVenue/fields/schedule/blacklist'
    client = app.test_client()
    response = client.delete(url, headers=header, json=body)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)

    assert response.status_code == 200
    assert response.get_json()['delete_status'] == True

def test_get_reservation_list_in_a_field():
    ## ==== Admin prerequirement ==== ###
    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_unittest_user()
    insert_unittest_token(admin_token, admin_device)
    insert_unittest_sport_venue(sport_venue, sport_kind)

    field_id = newFieldUUID()
    insert_unittest_field_to_venue(field_id, sport_venue, 1)

    ## Player prerequirements
    insert_player_unittest_user()
    insert_booking_unittest(newBookingUUID(), field_id, "2024-05-01", "09:00:00", "10:59:59")
    insert_booking_unittest(newBookingUUID(), field_id, "2024-05-04", "09:00:00", "10:59:59")
    insert_booking_unittest(newBookingUUID(), field_id, "2024-05-20", "09:00:00", "10:59:59")

    ## test

    header = {
        'token': admin_token
    }

    url = f"admin/sportVenue/fields/schedule/reservation/{field_id}/5/2024"

    client = app.test_client()
    response = client.get(url, headers=header)

    ## clean prereq
    delete_unittest_device(admin_device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)

    delete_player_unittest_user()

    ## validation
    assert response.status_code == 200
    assert response.get_json()['get_status'] == True

def test_get_sport_venue_by_id_success():
    """Test to get managed venue information by admin with valid request"""
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)

    client = app.test_client()
    url = f"/admin/sportVenue/{sport_venue}"

    header = {
        "token": token
    }

    response = client.get(url, headers=header)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True

def test_get_sport_venue_by_id_not_his_own():
    """Test to get managed venue information by admin with valid request"""
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)

    client = app.test_client()
    url = f"/admin/sportVenue/{newSportFieldUUID()}"

    header = {
        "token": token
    }

    response = client.get(url, headers=header)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)

    assert response.status_code == 403
    assert response.get_json()['get_status'] == False

def test_delete_sport_venue_by_id_success():
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)

    client = app.test_client()
    url = f"/admin/sportVenue/{sport_venue}"

    header = {
        "token": token
    }

    response = client.delete(url, headers=header)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)

    assert response.status_code == 200
    assert response.get_json()['delete_status'] == True

def test_delete_sport_venue_by_id_not_host():
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)

    device2 = newVirtualDeviceID()
    token2 = newUserToken()
    insert_unittest_device(device2)
    insert_unittest_user_custom('unittest2')
    insert_unittest_token_custom(token2, device2, 'unittest2')

    client = app.test_client()
    url = f"/admin/sportVenue/{sport_venue}"

    header = {
        "token": token2
    }

    response = client.delete(url, headers=header)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)
    delete_unittest_device(device2)
    delete_unittest_user_custom('unittest2')

    assert response.status_code == 403
    assert response.get_json()['delete_status'] == False

def test_delete_sport_venue_by_id_not_found():
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)

    client = app.test_client()
    url = f"/admin/sportVenue/{newSportFieldUUID()}"

    header = {
        "token": token
    }

    response = client.delete(url, headers=header)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)

    assert response.status_code == 404
    assert response.get_json()['delete_status'] == False

def test_get_album_by_owner():
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)
    insert_album_photo(sport_venue, 'file1', 'url1')
    insert_album_photo(sport_venue, 'file2', 'url2')
    insert_album_photo(sport_venue, 'file3', 'url3')

    client = app.test_client()
    url = f"/admin/sportVenue/{sport_venue}/album"

    header = {
        "token": token
    }

    response = client.get(url, headers=header)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True
    assert len(response.get_json()['data']) == 3

def test_get_album_by_owner_deleted_1():
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)
    insert_album_photo(sport_venue, 'file1', 'url1')
    insert_album_photo(sport_venue, 'file2', 'url2')
    insert_album_photo(sport_venue, 'file3', 'url3')
    soft_delete_photo_album(sport_venue, 'file2')

    client = app.test_client()
    url = f"/admin/sportVenue/{sport_venue}/album"

    header = {
        "token": token
    }

    response = client.get(url, headers=header)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True
    assert len(response.get_json()['data']) == 2

def test_get_album_by_not_owner():
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)
    insert_album_photo(sport_venue, 'file1', 'url1')
    insert_album_photo(sport_venue, 'file2', 'url2')
    insert_album_photo(sport_venue, 'file3', 'url3')

    username = 'adminunittest'
    device_2 = newVirtualDeviceID()
    token_2 = newUserToken()
    insert_unittest_device(device_2)
    insert_unittest_user_custom(username)
    insert_unittest_token_custom(token_2, device_2, username)

    client = app.test_client()
    url = f"/admin/sportVenue/{sport_venue}/album"

    header = {
        "token": token_2
    }

    response = client.get(url, headers=header)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)
    delete_unittest_user_custom(username)
    delete_unittest_device(device_2)

    assert response.status_code == 403
    assert response.get_json()['get_status'] == False
    assert response.get_json()['data'] == None

def test_get_album_by_token_expired():
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)
    insert_album_photo(sport_venue, 'file1', 'url1')
    insert_album_photo(sport_venue, 'file2', 'url2')
    insert_album_photo(sport_venue, 'file3', 'url3')

    client = app.test_client()
    url = f"/admin/sportVenue/{sport_venue}/album"

    header = {
        "token": newUserToken()
    }

    response = client.get(url, headers=header)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)

    assert response.status_code == 401
    assert response.get_json()['get_status'] == False
    assert response.get_json()['data'] == None

def test_delete_album_by_owner():
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)
    insert_album_photo(sport_venue, 'file1.jpg', 'url1')
    insert_album_photo(sport_venue, 'file2.heic', 'url2')
    insert_album_photo(sport_venue, 'file3.png', 'url3')

    client = app.test_client()
    url = f"/admin/sportVenue/{sport_venue}/album/file2.heic"

    header = {
        "token": token
    }

    response = client.delete(url, headers=header)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)

    assert response.status_code == 200
    assert response.get_json()['delete_status'] == True
    assert len(response.get_json()['data']) == 2

def test_delete_album_by_not_owner():
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)
    insert_album_photo(sport_venue, 'file1', 'url1')
    insert_album_photo(sport_venue, 'file2', 'url2')
    insert_album_photo(sport_venue, 'file3', 'url3')

    username = 'adminunittest'
    device_2 = newVirtualDeviceID()
    token_2 = newUserToken()
    insert_unittest_device(device_2)
    insert_unittest_user_custom(username)
    insert_unittest_token_custom(token_2, device_2, username)

    client = app.test_client()
    url = f"/admin/sportVenue/{sport_venue}/album/file2"

    header = {
        "token": token_2
    }

    response = client.delete(url, headers=header)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)
    delete_unittest_user_custom(username)
    delete_unittest_device(device_2)

    assert response.status_code == 403
    assert response.get_json()['delete_status'] == False
    assert response.get_json()['data'] == None

def test_delete_album_by_owner_filename_not_found():
    device = newVirtualDeviceID()
    token = newUserToken()
    sport_kind = insert_unittest_sport_kind()
    sport_venue = newSportFieldUUID()

    insert_unittest_device(device)
    insert_unittest_user()
    insert_unittest_token(token, device)
    insert_unittest_sport_venue(sport_venue, sport_kind)
    insert_album_photo(sport_venue, 'file1.jpg', 'url1')
    insert_album_photo(sport_venue, 'file2.heic', 'url2')
    insert_album_photo(sport_venue, 'file3.png', 'url3')

    client = app.test_client()
    url = f"/admin/sportVenue/{sport_venue}/album/file5.heic"

    header = {
        "token": token
    }

    response = client.delete(url, headers=header)

    delete_unittest_device(device)
    delete_unittest_user()
    delete_unittest_sport_kind(sport_kind)
    delete_unittest_sport_venue(sport_venue)

    assert response.status_code == 404
    assert response.get_json()['delete_status'] == False
    assert response.get_json()['data'] != None
