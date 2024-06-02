from static import *
from app import app

def test_create_match_history_by_host():
    # preparation
    device_admin = newVirtualDeviceID()
    insert_unittest_device(device_admin)
    insert_admin_unittest_user()
    token_admin = newUserToken()
    insert_admin_unittest_token(token_admin, device_admin)

    sport_kind_id = insert_admin_unittest_sport_kind()

    venue_id = newSportFieldUUID()
    insert_admin_unittest_sport_venue(venue_id, sport_kind_id)
    field_id = newSportFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, venue_id, 1)

    device_player = newVirtualDeviceID()
    insert_unittest_device(device_player)
    insert_player_unittest_user()
    token_player = newUserToken()
    insert_player_unittest_token(token_player, device_player)

    reservation_id = newBookingUUID()
    insert_booking_unittest(reservation_id, field_id, '2025-05-28', '09:00:00', '11:00:00')
    change_reservation_status(reservation_id, 'approved')

    # condition
    header = {
        'token': token_player
    }
    body = {
        'reservation_id': reservation_id,
        'match_number': 1
    }

    # test
    url = f"/player/reservation/match-history"
    client = app.test_client()
    response = client.post(url, headers=header, json=body)

    # clean test data
    delete_admin_unittest_user()
    delete_player_unittest_user()
    delete_unittest_device(device_admin)
    delete_unittest_device(device_player)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # assertion
    assert response.status_code == 200
    assert response.get_json()['status'] == True
    assert response.get_json()['data'] != None


def test_create_match_history_by_member():
    # preparation
    device_admin = newVirtualDeviceID()
    insert_unittest_device(device_admin)
    insert_admin_unittest_user()
    token_admin = newUserToken()
    insert_admin_unittest_token(token_admin, device_admin)

    sport_kind_id = insert_admin_unittest_sport_kind()

    venue_id = newSportFieldUUID()
    insert_admin_unittest_sport_venue(venue_id, sport_kind_id)
    field_id = newSportFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, venue_id, 1)

    device_player = newVirtualDeviceID()
    insert_unittest_device(device_player)
    insert_player_unittest_user()
    token_player = newUserToken()
    insert_player_unittest_token(token_player, device_player)

    reservation_id = newBookingUUID()
    insert_booking_unittest(reservation_id, field_id, '2025-05-28', '09:00:00', '11:00:00')
    change_reservation_status(reservation_id, 'approved')

    device_player_2 = newVirtualDeviceID()
    insert_unittest_device(device_player_2)
    username_player_2 = 'unittest2'
    insert_player_unittest_user_custom(username_player_2)
    token_player_2 = newUserToken()
    insert_player_unittest_token_custom(token_player_2, device_player_2, 'unittest2')
    insert_member_reservation(reservation_id, 'unittest2')

    # condition
    header = {
        'token': token_player_2
    }
    body = {
        'reservation_id': reservation_id,
        'match_number': 1
    }

    # test
    url = f"/player/reservation/match-history"
    client = app.test_client()
    response = client.post(url, headers=header, json=body)

    # clean test data
    delete_admin_unittest_user()
    delete_player_unittest_user()
    delete_unittest_device(device_admin)
    delete_unittest_device(device_player)
    delete_admin_unittest_sport_kind(sport_kind_id)

    delete_player_unittest_user_custom('unittest2')
    delete_unittest_device(device_player_2)

    # assertion
    assert response.status_code == 200
    assert response.get_json()['status'] == True
    assert response.get_json()['data'] != None

def test_create_match_history_by_not_member():
    # preparation
    device_admin = newVirtualDeviceID()
    insert_unittest_device(device_admin)
    insert_admin_unittest_user()
    token_admin = newUserToken()
    insert_admin_unittest_token(token_admin, device_admin)

    sport_kind_id = insert_admin_unittest_sport_kind()

    venue_id = newSportFieldUUID()
    insert_admin_unittest_sport_venue(venue_id, sport_kind_id)
    field_id = newSportFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, venue_id, 1)

    device_player = newVirtualDeviceID()
    insert_unittest_device(device_player)
    insert_player_unittest_user()
    token_player = newUserToken()
    insert_player_unittest_token(token_player, device_player)

    reservation_id = newBookingUUID()
    insert_booking_unittest(reservation_id, field_id, '2025-05-28', '09:00:00', '11:00:00')
    change_reservation_status(reservation_id, 'approved')

    device_player_2 = newVirtualDeviceID()
    insert_unittest_device(device_player_2)
    username_player_2 = 'unittest2'
    insert_player_unittest_user_custom(username_player_2)
    token_player_2 = newUserToken()
    insert_player_unittest_token_custom(token_player_2, device_player_2, 'unittest2')

    # condition
    header = {
        'token': token_player_2
    }
    body = {
        'reservation_id': reservation_id,
        'match_number': 1
    }

    # test
    url = f"/player/reservation/match-history"
    client = app.test_client()
    response = client.post(url, headers=header, json=body)

    # clean test data
    delete_admin_unittest_user()
    delete_player_unittest_user()
    delete_unittest_device(device_admin)
    delete_unittest_device(device_player)
    delete_admin_unittest_sport_kind(sport_kind_id)

    delete_player_unittest_user_custom('unittest2')
    delete_unittest_device(device_player_2)

    # assertion
    assert response.status_code == 403
    assert response.get_json()['status'] == False
    assert response.get_json()['data'] == None

def test_create_match_history_not_approved_reservation():
    # preparation
    device_admin = newVirtualDeviceID()
    insert_unittest_device(device_admin)
    insert_admin_unittest_user()
    token_admin = newUserToken()
    insert_admin_unittest_token(token_admin, device_admin)

    sport_kind_id = insert_admin_unittest_sport_kind()

    venue_id = newSportFieldUUID()
    insert_admin_unittest_sport_venue(venue_id, sport_kind_id)
    field_id = newSportFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, venue_id, 1)

    device_player = newVirtualDeviceID()
    insert_unittest_device(device_player)
    insert_player_unittest_user()
    token_player = newUserToken()
    insert_player_unittest_token(token_player, device_player)

    reservation_id = newBookingUUID()
    insert_booking_unittest(reservation_id, field_id, '2025-05-28', '09:00:00', '11:00:00')
    change_reservation_status(reservation_id, 'waiting_approval')

    # condition
    header = {
        'token': token_player
    }
    body = {
        'reservation_id': reservation_id,
        'match_number': 1
    }

    # test
    url = f"/player/reservation/match-history"
    client = app.test_client()
    response = client.post(url, headers=header, json=body)

    # clean test data
    delete_admin_unittest_user()
    delete_player_unittest_user()
    delete_unittest_device(device_admin)
    delete_unittest_device(device_player)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # assertion
    assert response.status_code == 403
    assert response.get_json()['status'] == False
    assert response.get_json()['message'] == f"Reservation {reservation_id} is not approved"
    assert response.get_json()['data'] == None

def test_get_match_history():
    # preparation
    device_admin = newVirtualDeviceID()
    insert_unittest_device(device_admin)
    insert_admin_unittest_user()
    token_admin = newUserToken()
    insert_admin_unittest_token(token_admin, device_admin)

    sport_kind_id = insert_admin_unittest_sport_kind()

    venue_id = newSportFieldUUID()
    insert_admin_unittest_sport_venue(venue_id, sport_kind_id)
    field_id = newSportFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, venue_id, 1)

    device_player = newVirtualDeviceID()
    insert_unittest_device(device_player)
    insert_player_unittest_user()
    token_player = newUserToken()
    insert_player_unittest_token(token_player, device_player)

    reservation_id = newBookingUUID()
    insert_booking_unittest(reservation_id, field_id, '2025-05-28', '09:00:00', '11:00:00')
    change_reservation_status(reservation_id, 'approved')

    # condition
    insert_new_match_history(reservation_id, 3)

    header = {
        'token': token_player
    }
    body = {
        'reservation_id': reservation_id
    }

    # test
    url = f"/player/reservation/match-history"
    client = app.test_client()
    response = client.get(url, headers=header, json=body)

    # clean test data
    delete_admin_unittest_user()
    delete_player_unittest_user()
    delete_unittest_device(device_admin)
    delete_unittest_device(device_player)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # assertion
    assert response.status_code == 200
    assert response.get_json()['status'] == True
    assert response.get_json()['data'] != None
    assert len(response.get_json()['data']) == 3

def test_get_match_history_2():
    # preparation
    device_admin = newVirtualDeviceID()
    insert_unittest_device(device_admin)
    insert_admin_unittest_user()
    token_admin = newUserToken()
    insert_admin_unittest_token(token_admin, device_admin)

    sport_kind_id = insert_admin_unittest_sport_kind()

    venue_id = newSportFieldUUID()
    insert_admin_unittest_sport_venue(venue_id, sport_kind_id)
    field_id = newSportFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, venue_id, 1)

    device_player = newVirtualDeviceID()
    insert_unittest_device(device_player)
    insert_player_unittest_user()
    token_player = newUserToken()
    insert_player_unittest_token(token_player, device_player)

    reservation_id = newBookingUUID()
    insert_booking_unittest(reservation_id, field_id, '2025-05-28', '09:00:00', '11:00:00')
    change_reservation_status(reservation_id, 'approved')

    # condition
    insert_new_match_history(reservation_id, 5)

    header = {
        'token': token_player
    }
    body = {
        'reservation_id': reservation_id
    }

    # test
    url = f"/player/reservation/match-history"
    client = app.test_client()
    response = client.get(url, headers=header, json=body)

    # clean test data
    delete_admin_unittest_user()
    delete_player_unittest_user()
    delete_unittest_device(device_admin)
    delete_unittest_device(device_player)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # assertion
    assert response.status_code == 200
    assert response.get_json()['status'] == True
    assert response.get_json()['data'] != None
    assert len(response.get_json()['data']) == 5