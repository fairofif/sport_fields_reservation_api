from db_config import mysql
import pymysql
from app import app
from dotenv import load_dotenv
load_dotenv()
import os
from token_generator import newUserToken
from virtual_device_id_generator import newVirtualDeviceID
from uuid_generator import newSportKindUUID, newSportFieldUUID, newFieldUUID, newBlacklistScheduleUUID, newBookingUUID

# ================= Static Method Player User ================ #

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

def insert_player_unittest_user_custom(username):
    ava_url = os.getenv("DEFAULT_AVA_PATH")

    query = 'INSERT INTO Player VALUES("'+username+'", "unittest", "Unit Test", "'+ava_url+'", CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), "08123456789")'
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def delete_player_unittest_user_custom(username):
    query = 'DELETE FROM Player WHERE username = "'+username+'"'
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

def insert_player_unittest_token_custom(token, device_id, username):
    query = f"INSERT INTO Player_Login_Token VALUES ('{token}', '{username}', CURRENT_TIMESTAMP(), '{device_id}')"
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

def insert_admin_unittest_blacklist(blacklist_id, field_id, date, fromTime, toTime, isEveryWeek):
    query = f"INSERT INTO Blacklist_Schedule VALUES ('{blacklist_id}', '{field_id}', '{date}', '{fromTime}', '{toTime}', {isEveryWeek}, 'Cuti Khusus', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP)"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def change_reservation_status(booking_id, status):
    query = f"UPDATE Reservation SET booking_status = '{status}' WHERE id = '{booking_id}'"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
#### ======================= UNIT TEST =========================== ####

def test_player_create_reservation_success():
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

    body = {
        "field_id": field_id,
        "name": "Mabar Anak Anak Kece",
        "mabar_type": "friendly",
        "date": "2024-05-01",
        "time_start": "13:00:00",
        "time_end": "16:59:59"
    }

    url = "/player/reservation"
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
    assert response.get_json()['create_status'] == True

def test_player_create_reservation_schedule_is_out_of_field_range():
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

    body = {
        "field_id": field_id,
        "name": "Mabar Anak Anak Kece",
        "mabar_type": "friendly",
        "date": "2024-05-01",
        "time_start": "01:00:00",
        "time_end": "16:59:59"
    }

    url = "/player/reservation"
    client = app.test_client()

    response = client.post(url, headers=header, json=body)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 409
    assert response.get_json()['create_status'] == False
    assert response.get_json()['message'] == "Schedule that you choose is out of range of this venue's open-closed time"

def test_player_create_reservation_schedule_is_take_by_other_1():
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

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")

    # ============ TEST ============= #

    header = {
        "token": player_token
    }

    body = {
        "field_id": field_id,
        "name": "Mabar Anak Anak Kece",
        "mabar_type": "friendly",
        "date": "2024-05-01",
        "time_start": "11:00:00",
        "time_end": "13:59:59"
    }

    url = "/player/reservation"
    client = app.test_client()

    response = client.post(url, headers=header, json=body)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 409
    assert response.get_json()['create_status'] == False
    assert response.get_json()['message'] == "Schedule that you choose is taken by others"

def test_player_create_reservation_schedule_is_take_by_other_2():
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

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")

    # ============ TEST ============= #

    header = {
        "token": player_token
    }

    body = {
        "field_id": field_id,
        "name": "Mabar Anak Anak Kece",
        "mabar_type": "friendly",
        "date": "2024-05-01",
        "time_start": "08:00:00",
        "time_end": "10:59:59"
    }

    url = "/player/reservation"
    client = app.test_client()

    response = client.post(url, headers=header, json=body)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 409
    assert response.get_json()['create_status'] == False
    assert response.get_json()['message'] == "Schedule that you choose is taken by others"

def test_player_create_reservation_schedule_is_take_by_other_3():
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

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")

    # ============ TEST ============= #

    header = {
        "token": player_token
    }

    body = {
        "field_id": field_id,
        "name": "Mabar Anak Anak Kece",
        "mabar_type": "friendly",
        "date": "2024-05-01",
        "time_start": "08:00:00",
        "time_end": "13:59:59"
    }

    url = "/player/reservation"
    client = app.test_client()

    response = client.post(url, headers=header, json=body)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 409
    assert response.get_json()['create_status'] == False
    assert response.get_json()['message'] == "Schedule that you choose is taken by others"

def test_player_create_reservation_schedule_on_blacklist_schedule_1():
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

    ## ============== condition requirement =============== #

    blacklist_id = newBlacklistScheduleUUID()
    insert_admin_unittest_blacklist(blacklist_id, field_id, "2024-05-01", "10:00:00", "13:59:59", 0)

    # ============ TEST ============= #

    header = {
        "token": player_token
    }

    body = {
        "field_id": field_id,
        "name": "Mabar Anak Anak Kece",
        "mabar_type": "friendly",
        "date": "2024-05-01",
        "time_start": "08:00:00",
        "time_end": "12:59:59"
    }

    url = "/player/reservation"
    client = app.test_client()

    response = client.post(url, headers=header, json=body)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 409
    assert response.get_json()['create_status'] == False
    assert response.get_json()['message'] == "Schedule that you choose is blaklisted by admin"

def test_player_create_reservation_schedule_on_blacklist_schedule_2():
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

    ## ============== condition requirement =============== #

    blacklist_id = newBlacklistScheduleUUID()
    insert_admin_unittest_blacklist(blacklist_id, field_id, "2024-05-01", "10:00:00", "13:59:59", 0)

    # ============ TEST ============= #

    header = {
        "token": player_token
    }

    body = {
        "field_id": field_id,
        "name": "Mabar Anak Anak Kece",
        "mabar_type": "friendly",
        "date": "2024-05-01",
        "time_start": "12:00:00",
        "time_end": "16:59:59"
    }

    url = "/player/reservation"
    client = app.test_client()

    response = client.post(url, headers=header, json=body)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 409
    assert response.get_json()['create_status'] == False
    assert response.get_json()['message'] == "Schedule that you choose is blaklisted by admin"

def test_player_create_reservation_schedule_on_blacklist_schedule_3():
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

    ## ============== condition requirement =============== #

    blacklist_id = newBlacklistScheduleUUID()
    insert_admin_unittest_blacklist(blacklist_id, field_id, "2024-05-01", "10:00:00", "13:59:59", 0)

    # ============ TEST ============= #

    header = {
        "token": player_token
    }

    body = {
        "field_id": field_id,
        "name": "Mabar Anak Anak Kece",
        "mabar_type": "friendly",
        "date": "2024-05-01",
        "time_start": "08:00:00",
        "time_end": "16:59:59"
    }

    url = "/player/reservation"
    client = app.test_client()

    response = client.post(url, headers=header, json=body)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 409
    assert response.get_json()['create_status'] == False
    assert response.get_json()['message'] == "Schedule that you choose is blaklisted by admin"

def test_player_create_reservation_schedule_on_blacklist_schedule_every_week_1():
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

    ## ============== condition requirement =============== #

    blacklist_id = newBlacklistScheduleUUID()
    insert_admin_unittest_blacklist(blacklist_id, field_id, "2024-04-01", "10:00:00", "13:59:59", 1)

    # ============ TEST ============= #

    header = {
        "token": player_token
    }

    body = {
        "field_id": field_id,
        "name": "Mabar Anak Anak Kece",
        "mabar_type": "friendly",
        "date": "2024-05-20",
        "time_start": "08:00:00",
        "time_end": "12:59:59"
    }

    url = "/player/reservation"
    client = app.test_client()

    response = client.post(url, headers=header, json=body)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 409
    assert response.get_json()['create_status'] == False
    assert response.get_json()['message'] == "Schedule that you choose is blaklisted by admin"

def test_player_create_reservation_schedule_on_blacklist_schedule_every_week_2():
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

    ## ============== condition requirement =============== #

    blacklist_id = newBlacklistScheduleUUID()
    insert_admin_unittest_blacklist(blacklist_id, field_id, "2024-04-01", "10:00:00", "13:59:59", 1)

    # ============ TEST ============= #

    header = {
        "token": player_token
    }

    body = {
        "field_id": field_id,
        "name": "Mabar Anak Anak Kece",
        "mabar_type": "friendly",
        "date": "2024-05-20",
        "time_start": "12:00:00",
        "time_end": "16:59:59"
    }

    url = "/player/reservation"
    client = app.test_client()

    response = client.post(url, headers=header, json=body)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 409
    assert response.get_json()['create_status'] == False
    assert response.get_json()['message'] == "Schedule that you choose is blaklisted by admin"

def test_player_create_reservation_schedule_on_blacklist_schedule_every_week_3():
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

    ## ============== condition requirement =============== #

    blacklist_id = newBlacklistScheduleUUID()
    insert_admin_unittest_blacklist(blacklist_id, field_id, "2024-04-01", "10:00:00", "13:59:59", 1)

    # ============ TEST ============= #

    header = {
        "token": player_token
    }

    body = {
        "field_id": field_id,
        "name": "Mabar Anak Anak Kece",
        "mabar_type": "friendly",
        "date": "2024-05-20",
        "time_start": "08:00:00",
        "time_end": "16:59:59"
    }

    url = "/player/reservation"
    client = app.test_client()

    response = client.post(url, headers=header, json=body)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 409
    assert response.get_json()['create_status'] == False
    assert response.get_json()['message'] == "Schedule that you choose is blaklisted by admin"

def test_player_cancel_reservation_on_waiting_approval():
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

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'waiting_approval')

    ## TEST
    header = {
        'token': player_token
    }

    url = f"/player/reservation/cancel/{booking_id}"
    client = app.test_client()

    response = client.put(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['edit_status'] == True
    assert response.get_json()['message'] == f"Reservation {booking_id} has been cancelled successfully"


def test_player_cancel_reservation_on_payment():
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

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'payment')

    ## TEST
    header = {
        'token': player_token
    }

    url = f"/player/reservation/cancel/{booking_id}"
    client = app.test_client()

    response = client.put(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['edit_status'] == True
    assert response.get_json()['message'] == f"Reservation {booking_id} has been cancelled successfully"

def test_player_cancel_reservation_on_other_status():
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

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')

    ## TEST
    header = {
        'token': player_token
    }

    url = f"/player/reservation/cancel/{booking_id}"
    client = app.test_client()

    response = client.put(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 403
    assert response.get_json()['edit_status'] == False
    assert response.get_json()['message'] == "Reservation with booking_status = 'approved' cannot be cancelled"

def test_player_change_open_member_status_on_approved_status_to_open():
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

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')

    ## TEST
    header = {
        'token': player_token
    }

    url = f"/player/reservation/open/{booking_id}/1"
    client = app.test_client()

    response = client.put(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['edit_status'] == True
    assert response.get_json()['message'] == f"Reservation {booking_id} now is open member"

def test_player_change_open_member_status_to_closed():
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

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')

    ## TEST
    header = {
        'token': player_token
    }

    url = f"/player/reservation/open/{booking_id}/0"
    client = app.test_client()

    response = client.put(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['edit_status'] == True
    assert response.get_json()['message'] == f"Reservation {booking_id} now is closed member"

def test_player_change_open_member_status_on_except_approved_status_to_open():
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

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'waiting_approval')

    ## TEST
    header = {
        'token': player_token
    }

    url = f"/player/reservation/open/{booking_id}/1"
    client = app.test_client()

    response = client.put(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 403
    assert response.get_json()['edit_status'] == False
    assert response.get_json()['message'] == f"Only approved reservation could open member"

def test_player_change_open_member_status_not_host():
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

    ## ============== condition requirement =============== #

    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2024-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'waiting_approval')

    player2token = newUserToken()

    player2device = newVirtualDeviceID()
    insert_player_unittest_user_custom("not_host")
    insert_unittest_device(player2device)
    insert_player_unittest_token_custom(player2token, player2device, "not_host")

    ## TEST
    header = {
        'token': player2token
    }

    url = f"/player/reservation/open/{booking_id}/1"
    client = app.test_client()

    response = client.put(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(player2device)
    delete_player_unittest_user_custom("not_host")

    # =========== VALIDATION =========== #

    assert response.status_code == 401
    assert response.get_json()['edit_status'] == False
    assert response.get_json()['message'] == f"Only host could edit open member status of reservation"
