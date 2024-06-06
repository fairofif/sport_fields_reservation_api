from static import *
from app import app

FOLDER_QR = os.getenv('FOLDER_QR')

def test_get_reservation_details_if_member():
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
    change_open_member_status(booking_id, 1)

    username_join = "wakacipuyyy"
    insert_player_unittest_user_custom(username_join)
    token_join = newUserToken()
    device_join = newVirtualDeviceID()
    insert_unittest_device(device_join)
    insert_player_unittest_token_custom(token_join, device_join, username_join)
    insert_member_reservation(booking_id, username_join)

    ## TEST

    url = f"/player/reservation/details/{booking_id}"

    header = {
        'token': token_join
    }

    client = app.test_client()

    response = client.get(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_join)
    delete_player_unittest_user_custom(username_join)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True
    assert response.get_json()['message'] == f"Retrieve reservation info successfully"
    assert response.get_json()['data']['info'] != None
    assert response.get_json()['data']['role'] == 'member'

def test_get_reservation_details_if_host():
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
    change_open_member_status(booking_id, 1)

    username_join = "wakacipuyyy"
    insert_player_unittest_user_custom(username_join)
    token_join = newUserToken()
    device_join = newVirtualDeviceID()
    insert_unittest_device(device_join)
    insert_player_unittest_token_custom(token_join, device_join, username_join)
    insert_member_reservation(booking_id, username_join)

    ## TEST

    url = f"/player/reservation/details/{booking_id}"

    header = {
        'token': player_token
    }

    client = app.test_client()

    response = client.get(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_join)
    delete_player_unittest_user_custom(username_join)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True
    assert response.get_json()['message'] == f"Retrieve reservation info successfully"
    assert response.get_json()['data']['info'] != None
    assert response.get_json()['data']['role'] == 'host'

def test_get_reservation_details_if_not_a_member_but_reservation_public():
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
    change_open_member_status(booking_id, 1)
    change_is_public_status(booking_id, 1)

    username_join = "wakacipuyyy"
    insert_player_unittest_user_custom(username_join)
    token_join = newUserToken()
    device_join = newVirtualDeviceID()
    insert_unittest_device(device_join)
    insert_player_unittest_token_custom(token_join, device_join, username_join)

    ## TEST

    url = f"/player/reservation/details/{booking_id}"

    header = {
        'token': token_join
    }

    client = app.test_client()

    response = client.get(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_join)
    delete_player_unittest_user_custom(username_join)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True
    assert response.get_json()['message'] == f"Retrieve reservation info successfully"
    assert response.get_json()['data']['info'] != None
    assert response.get_json()['data']['role'] == 'guest'

def test_get_reservation_details_if_not_a_member_but_reservation_not_public():
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
    change_open_member_status(booking_id, 1)
    change_is_public_status(booking_id, 0)

    username_join = "wakacipuyyy"
    insert_player_unittest_user_custom(username_join)
    token_join = newUserToken()
    device_join = newVirtualDeviceID()
    insert_unittest_device(device_join)
    insert_player_unittest_token_custom(token_join, device_join, username_join)

    ## TEST

    url = f"/player/reservation/details/{booking_id}"

    header = {
        'token': token_join
    }

    client = app.test_client()

    response = client.get(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_join)
    delete_player_unittest_user_custom(username_join)

    # =========== VALIDATION =========== #

    assert response.status_code == 403
    assert response.get_json()['get_status'] == False
    assert response.get_json()['message'] == f"Retrieve reservation info unsuccessfully"
    assert response.get_json()['data']['info'] == None
    assert response.get_json()['data']['role'] == None

def test_get_qr_by_id_reservation_by_member():
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
    change_open_member_status(booking_id, 1)

    username_join = "wakacipuyyy"
    insert_player_unittest_user_custom(username_join)
    token_join = newUserToken()
    device_join = newVirtualDeviceID()
    insert_unittest_device(device_join)
    insert_player_unittest_token_custom(token_join, device_join, username_join)
    insert_member_reservation(booking_id, username_join)

    ## TEST

    url = f"/player/reservation/QR/{booking_id}"

    header = {
        'token': token_join
    }

    client = app.test_client()

    response = client.post(url, headers=header)

    # =========== Clean data TEST ============ #

    os.remove(f"{FOLDER_QR}/{booking_id}.png")
    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_join)
    delete_player_unittest_user_custom(username_join)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True
    assert response.get_json()['message'] == f"New QR Created successfully"
    assert response.get_json()['data'] != None

def test_get_qr_by_id_reservation_by_host():
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
    change_open_member_status(booking_id, 1)

    username_join = "wakacipuyyy"
    insert_player_unittest_user_custom(username_join)
    token_join = newUserToken()
    device_join = newVirtualDeviceID()
    insert_unittest_device(device_join)
    insert_player_unittest_token_custom(token_join, device_join, username_join)
    insert_member_reservation(booking_id, username_join)

    ## TEST

    url = f"/player/reservation/QR/{booking_id}"

    header = {
        'token': player_token
    }

    client = app.test_client()

    response = client.post(url, headers=header)

    # =========== Clean data TEST ============ #

    os.remove(f"{FOLDER_QR}/{booking_id}.png")
    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_join)
    delete_player_unittest_user_custom(username_join)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True
    assert response.get_json()['message'] == f"New QR Created successfully"
    assert response.get_json()['data'] != None

def test_get_qr_by_id_reservation_by_member_created_before():
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
    change_open_member_status(booking_id, 1)

    username_join = "wakacipuyyy"
    insert_player_unittest_user_custom(username_join)
    token_join = newUserToken()
    device_join = newVirtualDeviceID()
    insert_unittest_device(device_join)
    insert_player_unittest_token_custom(token_join, device_join, username_join)
    insert_member_reservation(booking_id, username_join)

    insert_QR_records_unittest(booking_id)

    ## TEST

    url = f"/player/reservation/QR/{booking_id}"

    header = {
        'token': token_join
    }

    client = app.test_client()

    response = client.post(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_join)
    delete_player_unittest_user_custom(username_join)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True
    assert response.get_json()['message'] == f"QR had created before, get QR successfully"
    assert response.get_json()['data'] != None

def test_get_qr_by_id_reservation_by_not_admin_not_member():
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
    change_open_member_status(booking_id, 1)

    username_join = "wakacipuyyy"
    insert_player_unittest_user_custom(username_join)
    token_join = newUserToken()
    device_join = newVirtualDeviceID()
    insert_unittest_device(device_join)
    insert_player_unittest_token_custom(token_join, device_join, username_join)


    ## TEST

    url = f"/player/reservation/QR/{booking_id}"

    header = {
        'token': token_join
    }

    client = app.test_client()

    response = client.post(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_join)
    delete_player_unittest_user_custom(username_join)

    # =========== VALIDATION =========== #

    assert response.status_code == 403
    assert response.get_json()['get_status'] == False
    assert response.get_json()['message'] == f"This user is not host or member of reservation {booking_id}"
    assert response.get_json()['data'] == None


def test_get_qr_by_id_reservation_by_member_not_approved_yet():
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

    url = f"/player/reservation/QR/{booking_id}"

    header = {
        'token': player_token
    }

    client = app.test_client()

    response = client.post(url, headers=header)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)\

    # =========== VALIDATION =========== #

    assert response.status_code == 403
    assert response.get_json()['get_status'] == False
    assert response.get_json()['message'] == f"Reservation {booking_id} not approved yet"
    assert response.get_json()['data'] == None
