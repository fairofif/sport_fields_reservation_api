from db_config import mysql
import pymysql
from app import app
from dotenv import load_dotenv
load_dotenv()
import os
from token_generator import newUserToken
from virtual_device_id_generator import newVirtualDeviceID
from uuid_generator import newSportKindUUID, newSportFieldUUID, newFieldUUID, newBlacklistScheduleUUID, newBookingUUID

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

def delete_player_unittest_token(token):
    query = "DELETE FROM Player_Login_Token WHERE token = '"+token+"'"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def insert_player_unittest_token(token, device_id):
    query = "INSERT INTO Player_Login_Token VALUES ('"+token+"', 'unittest', CURRENT_TIMESTAMP(), '"+device_id+"')"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

## =============== Static Method Admin User ============== ##
def insert_admin_unittest_user():
    ava_url = os.getenv("DEFAULT_AVA_PATH")

    query = 'INSERT INTO Admin VALUES("unittest", "Unit Test", "unittest", "unittest", "'+ava_url+'", CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP())'
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def changeIsPublic(venue_id, status):
    query = f"UPDATE Sport_Field SET is_public = {status} WHERE id = '{venue_id}'"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def delete_admin_unittest_user():
    query = 'DELETE FROM Admin WHERE username = "unittest"'
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def insert_admin_unittest_token(token, device_id):
    query = "INSERT INTO Admin_Login_Token VALUES ('"+token+"', 'unittest', CURRENT_TIMESTAMP(), '"+device_id+"')"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def insert_admin_unittest_sport_kind():
    uuid = newSportKindUUID()
    query = "INSERT INTO Sport_Kind (id, name) VALUES ('"+uuid+"', 'unittest_sport')"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
    return uuid

def delete_admin_unittest_sport_kind(uuid):
    query = "DELETE FROM Sport_Kind WHERE id = '"+uuid+"'"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def insert_admin_unittest_sport_venue(venue_id, sport_kind_id):
    query = "INSERT INTO Sport_Field VALUES ('"+venue_id+"', 'unittest', '"+sport_kind_id+"', 'unittest', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), '-6.300012, 107.164228', 1, 1, 1, 'unittest', 'unittest', '08:00:00', '23:00:00', 40000)"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def insert_admin_unittest_field_to_venue(field_id, venue_id, number):
    query = "INSERT INTO Fields VALUES ('"+field_id+"', '"+venue_id+"', "+str(number)+", CURRENT_TIMESTAMP())"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def insert_admin_unittest_blacklist_one_time_only(blacklist_id, field_id):
    query = f"INSERT INTO Blacklist_Schedule VALUES ('{blacklist_id}', '{field_id}', '2024-07-20', '08:00:00', '11:00:00', 0, 'Cuti Khusus', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP)"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def insert_admin_unittest_blacklist_every_week(blacklist_id, field_id):
    query = f"INSERT INTO Blacklist_Schedule VALUES ('{blacklist_id}', '{field_id}', '2024-07-02', '08:00:00', '11:00:00', 1, 'Cuti Khusus', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP)"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def insert_admin_unittest_field_to_venue(field_id, venue_id, number):
    query = "INSERT INTO Fields VALUES ('"+field_id+"', '"+venue_id+"', "+str(number)+", CURRENT_TIMESTAMP())"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def delete_admin_unittest_field_from_venue(field_id):
    query = "DELETE FROM Fields WHERE id = '"+field_id+"'"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def insert_admin_unittest_blacklist_one_time_only(blacklist_id, field_id):
    query = f"INSERT INTO Blacklist_Schedule VALUES ('{blacklist_id}', '{field_id}', '2024-07-20', '08:00:00', '11:00:00', 0, 'Cuti Khusus', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP)"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def insert_admin_unittest_blacklist_every_week(blacklist_id, field_id):
    query = f"INSERT INTO Blacklist_Schedule VALUES ('{blacklist_id}', '{field_id}', '2024-07-20', '08:00:00', '11:00:00', 1, 'Cuti Khusus', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP)"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def delete_admin_unittest_delete_blacklist(blacklist_id):
    query = f"DELETE FROM Blacklist_Schedule WHERE id = '{blacklist_id}'"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

## =============== Static Method All User ================ ##

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

def insert_booking_unittest(book_id, field_id, date, time_start, time_end):
    query = "INSERT INTO Reservation (id, Field_id, Player_username, name, mabar_type, date, time_start, time_end, created_at, last_updated) VALUES "
    query = query + f"('{book_id}', '{field_id}', 'unittest', 'Mabar Orang Ganteng', 'friendly', '{date}', '{time_start}', '{time_end}', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP())"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

#### ======================= UNIT TEST =========================== ####

def test_get_venue_info_default():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    # ============ TEST ============= #

    header = {
        "token": player_token
    }

    body = {
        "is_car_parking": None,
        "is_bike_parking": None,
        "name": None,
        "Sport_Kind_id": None,
        "sort_by": None,
        "coordinate": None
    }

    url = "/player/sportVenue"
    client = app.test_client()

    response = client.post(url, headers=header, json=body)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True

def test_get_venue_info_with_conditional_filters():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    # ============ TEST ============= #

    header = {
        "token": player_token
    }

    body = {
        "is_car_parking": True,
        "is_bike_parking": True,
        "name": None,
        "Sport_Kind_id": None,
        "sort_by": None,
        "coordinate": None
    }

    url = "/player/sportVenue"
    client = app.test_client()

    response = client.post(url, headers=header, json=body)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True

def test_get_venue_info_with_sorting_option():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    # ============ TEST ============= #

    header = {
        "token": player_token
    }

    body = {
        "is_car_parking": False,
        "is_bike_parking": False,
        "name": None,
        "Sport_Kind_id": None,
        "sort_by": "distance",
        "coordinate": "-6.894797, 107.610590"
    }

    url = "/player/sportVenue"
    client = app.test_client()

    response = client.post(url, headers=header, json=body)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True

def test_get_venue_info_with_conditional_filters_and_sort():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    # ============ TEST ============= #

    header = {
        "token": player_token
    }

    body = {
        "is_car_parking": True,
        "is_bike_parking": True,
        "name": None,
        "Sport_Kind_id": None,
        "sort_by": "distance",
        "coordinate": "-6.894797, 107.610590"
    }

    url = "/player/sportVenue"
    client = app.test_client()

    response = client.post(url, headers=header, json=body)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True

def test_player_get_fields_list():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, sport_venue_id, 1)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    # ============ TEST ============= #

    header = {
        "token": player_token
    }

    url = f"/player/sportVenue/fields/{sport_venue_id}"
    client = app.test_client()

    response = client.get(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True

def test_player_get_blacklist_schedule():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, sport_venue_id, 1)

    blacklist_id_1 = newBlacklistScheduleUUID()
    blacklist_id_2 = newBlacklistScheduleUUID()
    insert_admin_unittest_blacklist_every_week(blacklist_id_1, field_id)
    insert_admin_unittest_blacklist_one_time_only(blacklist_id_2, field_id)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    # ============ TEST ============= #

    header = {
        "token": player_token
    }

    url = f"/player/sportVenue/fields/schedule/blacklist/{field_id}/7/2024"
    client = app.test_client()

    response = client.get(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True

def test_player_get_reservation_in_a_fields():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, sport_venue_id, 1)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    # ========= CONDITION prereq ================ #
    insert_booking_unittest(newBookingUUID(), field_id, "2024-05-01", "09:00:00", "10:59:59")
    insert_booking_unittest(newBookingUUID(), field_id, "2024-05-04", "09:00:00", "10:59:59")
    insert_booking_unittest(newBookingUUID(), field_id, "2024-05-20", "09:00:00", "10:59:59")

    # ============ TEST ============= #

    header = {
        "token": player_token
    }

    url = f"/player/sportVenue/fields/schedule/reservation/{field_id}/5/2024"
    client = app.test_client()

    response = client.get(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True

def test_player_get_venue_by_id():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)
    changeIsPublic(sport_venue_id, 1)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    # ============ TEST ============= #

    header = {
        "token": player_token
    }

    body = {
        'coordinate': "-6.894797, 107.610590"
    }

    url = f"/player/sportVenue/{sport_venue_id}"
    client = app.test_client()

    response = client.get(url, headers=header, json=body)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True

def test_player_get_venue_by_id_not_found():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)
    changeIsPublic(sport_venue_id, 1)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    # ============ TEST ============= #

    header = {
        "token": player_token
    }
    body = {
        'coordinate': "-6.894797, 107.610590"
    }

    url = f"/player/sportVenue/{newSportFieldUUID()}"
    client = app.test_client()

    response = client.get(url, headers=header, json=body)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 404
    assert response.get_json()['get_status'] == False

def test_player_get_venue_by_id_not_public():
    ## ============ admin prerequirement ============= #

    admin_device = newVirtualDeviceID()
    admin_token = newUserToken()

    sport_kind_id = insert_admin_unittest_sport_kind()
    sport_venue_id = newSportFieldUUID()

    insert_unittest_device(admin_device)
    insert_admin_unittest_user()
    insert_admin_unittest_token(admin_token, admin_device)
    insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)
    changeIsPublic(sport_venue_id, 0)

    ## ============ player prerequirement ============= #

    player_device = newVirtualDeviceID()
    player_token = newUserToken()
    insert_unittest_device(player_device)
    insert_player_unittest_user()
    insert_player_unittest_token(player_token, player_device)

    # ============ TEST ============= #

    header = {
        "token": player_token
    }
    body = {
        'coordinate': "-6.894797, 107.610590"
    }

    url = f"/player/sportVenue/{sport_venue_id}"
    client = app.test_client()

    response = client.get(url, headers=header, json=body)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 403
    assert response.get_json()['get_status'] == False
