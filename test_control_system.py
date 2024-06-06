from static import *
from app import app

# ============= UNIT TEST ============ #
def test_get_username_that_playing_on_a_field_with_schedule_on_schedule_1():
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

    url = f"/controlsystem/hostinfo/{field_id}/2024-05-01/09:00:00"
    client = app.test_client()

    response = client.get(url)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True
    assert response.get_json()['message'] == "There is ongoing schedule"
    assert response.get_json()['data'] != None

def test_get_username_that_playing_on_a_field_with_schedule_on_schedule_2():
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

    url = f"/controlsystem/hostinfo/{field_id}/2024-05-01/10:00:00"
    client = app.test_client()

    response = client.get(url)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True
    assert response.get_json()['message'] == "There is ongoing schedule"
    assert response.get_json()['data'] != None

def test_get_username_that_playing_on_a_field_with_schedule_outside_schedule_1():
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

    url = f"/controlsystem/hostinfo/{field_id}/2024-05-01/12:00:00"
    client = app.test_client()

    response = client.get(url)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True
    assert response.get_json()['message'] == "There isn't any ongoing schedule"
    assert response.get_json()['data'] == None

def test_get_username_that_playing_on_a_field_with_schedule_outside_schedule_2():
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

    url = f"/controlsystem/hostinfo/{field_id}/2024-05-01/08:00:00"
    client = app.test_client()

    response = client.get(url)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 200
    assert response.get_json()['get_status'] == True
    assert response.get_json()['message'] == "There isn't any ongoing schedule"
    assert response.get_json()['data'] == None

# def test_unlock_door_by_reservation_id():
#     ## ============ admin prerequirement ============= #

#     admin_device = newVirtualDeviceID()
#     admin_token = newUserToken()

#     sport_kind_id = insert_admin_unittest_sport_kind()
#     sport_venue_id = newSportFieldUUID()

#     insert_unittest_device(admin_device)
#     insert_admin_unittest_user()
#     insert_admin_unittest_token(admin_token, admin_device)
#     insert_admin_unittest_sport_venue(sport_venue_id, sport_kind_id)

#     field_id = newFieldUUID()
#     insert_admin_unittest_field_to_venue(field_id, sport_venue_id, 1)

#     ## ============ player prerequirement ============= #

#     player_device = newVirtualDeviceID()
#     player_token = newUserToken()
#     insert_unittest_device(player_device)
#     insert_player_unittest_user()
#     insert_player_unittest_token(player_token, player_device)

#     ## ============== condition requirement =============== #

#     booking_id = newBookingUUID()
#     insert_booking_unittest(booking_id, field_id, get_current_date(), "09:00:00", "11:59:59")
#     change_reservation_status(booking_id, 'approved')

#     ## TEST

#     url = f"/controlsystem/unlock/{sport_venue_id}/{booking_id}"
#     client = app.test_client()

#     response = client.get(url)

#     # =========== Clean data TEST ============ #

#     delete_player_unittest_user()
#     delete_admin_unittest_user()
#     delete_unittest_device(admin_device)
#     delete_unittest_device(player_device)
#     delete_admin_unittest_sport_kind(sport_kind_id)

#     # =========== VALIDATION =========== #

#     assert response.status_code == 200
#     assert response.get_json()['unlock_status'] == True
#     assert response.get_json()['message'] == "Reservation ID is valid, unlock granted"
#     assert response.get_json()['data'] != None

def test_unlock_door_by_reservation_id_not_in_schedule():
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
    insert_booking_unittest(booking_id, field_id, "2023-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')

    ## TEST

    url = f"/controlsystem/unlock/{sport_venue_id}/{booking_id}"
    client = app.test_client()

    response = client.get(url)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 403
    assert response.get_json()['unlock_status'] == False
    assert response.get_json()['message'] == "Reservation ID is not for today, unlock not granted"
    assert response.get_json()['data'] == None


def test_unlock_door_by_reservation_id_not_found():
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
    insert_booking_unittest(booking_id, field_id, "2023-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')

    ## TEST

    url = f"/controlsystem/unlock/{sport_venue_id}/{newBookingUUID()}"
    client = app.test_client()

    response = client.get(url)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 404
    assert response.get_json()['unlock_status'] == False
    assert response.get_json()['message'] == "Reservation ID is not found, unlock not granted"
    assert response.get_json()['data'] == None

def test_unlock_door_by_reservation_id_not_approved():
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
    insert_booking_unittest(booking_id, field_id, "2023-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'payment')

    ## TEST

    url = f"/controlsystem/unlock/{sport_venue_id}/{booking_id}"
    client = app.test_client()

    response = client.get(url)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 403
    assert response.get_json()['unlock_status'] == False
    assert response.get_json()['message'] == "Reservation ID is not approved/not approved yet, unlock not granted"
    assert response.get_json()['data'] == None

def test_unlock_door_by_reservation_id_not_matched_with_venue():
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
    insert_booking_unittest(booking_id, field_id, "2023-05-01", "09:00:00", "11:59:59")
    change_reservation_status(booking_id, 'approved')

    ## TEST

    url = f"/controlsystem/unlock/{newSportFieldUUID()}/{booking_id}"
    client = app.test_client()

    response = client.get(url)

    # =========== Clean data TEST ============ #

    delete_player_unittest_user()
    delete_admin_unittest_user()
    delete_unittest_device(admin_device)
    delete_unittest_device(player_device)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # =========== VALIDATION =========== #

    assert response.status_code == 403
    assert response.get_json()['unlock_status'] == False
    assert response.get_json()['message'] == "Reservation ID is not match with this venue, unlock not granted"
    assert response.get_json()['data'] == None
