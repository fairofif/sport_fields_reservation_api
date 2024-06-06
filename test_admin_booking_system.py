from static import *
from app import app

def test_get_all_reservation_from_player():
    # Player prerequirements
    insert_player_unittest_user()
    p_device_id = newVirtualDeviceID()
    p_token = newUserToken()
    insert_unittest_device(p_device_id)
    insert_player_unittest_token(p_token, p_device_id)

    # Admin prerequirements
    insert_admin_unittest_user()
    a_device_id = newVirtualDeviceID()
    insert_unittest_device(a_device_id)
    a_token = newUserToken()
    insert_admin_unittest_token(a_token, a_device_id)
    venue_id = newSportFieldUUID()
    sport_kind_id = insert_admin_unittest_sport_kind()
    insert_admin_unittest_sport_venue(venue_id, sport_kind_id)
    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, venue_id, 1)

    # Conditiion prerequirements
    insert_booking_unittest(newBookingUUID(), field_id, "2025-03-26", "13:00:00", "14:59:59")
    insert_booking_unittest(newBookingUUID(), field_id, "2025-03-27", "13:00:00", "14:59:59")
    insert_booking_unittest(newBookingUUID(), field_id, "2025-03-28", "13:00:00", "14:59:59")

    # test
    header = {
        'token': a_token
    }

    url = '/admin/reservation/payment'

    client = app.test_client()

    response = client.get(url, headers=header)

    # clean
    delete_admin_unittest_user()
    delete_player_unittest_user()
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(a_device_id)
    delete_unittest_device(p_device_id)

    # validation
    assert response.status_code == 200
    assert response.get_json()['get_status'] == True

def test_get_filtered_venue_reservation_from_player():
    # Player prerequirements
    insert_player_unittest_user()
    p_device_id = newVirtualDeviceID()
    p_token = newUserToken()
    insert_unittest_device(p_device_id)
    insert_player_unittest_token(p_token, p_device_id)

    # Admin prerequirements
    insert_admin_unittest_user()
    a_device_id = newVirtualDeviceID()
    insert_unittest_device(a_device_id)
    a_token = newUserToken()
    insert_admin_unittest_token(a_token, a_device_id)
    venue_id = newSportFieldUUID()
    sport_kind_id = insert_admin_unittest_sport_kind()
    insert_admin_unittest_sport_venue(venue_id, sport_kind_id)
    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, venue_id, 1)

    # Conditiion prerequirements
    insert_booking_unittest(newBookingUUID(), field_id, "2025-03-26", "13:00:00", "14:59:59")
    insert_booking_unittest(newBookingUUID(), field_id, "2025-03-27", "13:00:00", "14:59:59")
    book_approved = newBookingUUID()
    insert_booking_unittest(book_approved, field_id, "2025-03-28", "13:00:00", "14:59:59")
    change_reservation_status(book_approved, 'approved')

    # test
    header = {
        'token': a_token
    }

    url = f"/admin/reservation/{venue_id}/all"

    client = app.test_client()

    response = client.get(url, headers=header)

    # clean
    delete_admin_unittest_user()
    delete_player_unittest_user()
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(a_device_id)
    delete_unittest_device(p_device_id)

    # validation
    assert response.status_code == 200
    assert response.get_json()['get_status'] == True
    assert len(response.get_json()['data']) == 3

def test_get_filtered_venue_reservation_from_player_approved():
    # Player prerequirements
    insert_player_unittest_user()
    p_device_id = newVirtualDeviceID()
    p_token = newUserToken()
    insert_unittest_device(p_device_id)
    insert_player_unittest_token(p_token, p_device_id)

    # Admin prerequirements
    insert_admin_unittest_user()
    a_device_id = newVirtualDeviceID()
    insert_unittest_device(a_device_id)
    a_token = newUserToken()
    insert_admin_unittest_token(a_token, a_device_id)
    venue_id = newSportFieldUUID()
    sport_kind_id = insert_admin_unittest_sport_kind()
    insert_admin_unittest_sport_venue(venue_id, sport_kind_id)
    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, venue_id, 1)

    # Conditiion prerequirements
    insert_booking_unittest(newBookingUUID(), field_id, "2025-03-26", "13:00:00", "14:59:59")
    insert_booking_unittest(newBookingUUID(), field_id, "2025-03-27", "13:00:00", "14:59:59")
    book_approved = newBookingUUID()
    insert_booking_unittest(book_approved, field_id, "2025-03-28", "13:00:00", "14:59:59")
    change_reservation_status(book_approved, 'approved')

    # test
    header = {
        'token': a_token
    }

    url = f"/admin/reservation/{venue_id}/approved"

    client = app.test_client()

    response = client.get(url, headers=header)

    # clean
    delete_admin_unittest_user()
    delete_player_unittest_user()
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(a_device_id)
    delete_unittest_device(p_device_id)

    # validation
    assert response.status_code == 200
    assert response.get_json()['get_status'] == True
    assert len(response.get_json()['data']) == 1

def test_admin_get_detailed_reservation():
    # Player prerequirements
    insert_player_unittest_user()
    p_device_id = newVirtualDeviceID()
    p_token = newUserToken()
    insert_unittest_device(p_device_id)
    insert_player_unittest_token(p_token, p_device_id)

    # Admin prerequirements
    insert_admin_unittest_user()
    a_device_id = newVirtualDeviceID()
    insert_unittest_device(a_device_id)
    a_token = newUserToken()
    insert_admin_unittest_token(a_token, a_device_id)
    venue_id = newSportFieldUUID()
    sport_kind_id = insert_admin_unittest_sport_kind()
    insert_admin_unittest_sport_venue(venue_id, sport_kind_id)
    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, venue_id, 1)

    # Conditiion prerequirements
    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2025-03-26", "13:00:00", "14:59:59")

    # test
    header = {
        'token': a_token
    }

    url = f"/admin/reservation/detail/{booking_id}"

    client = app.test_client()

    response = client.get(url, headers=header)

    # clean
    delete_admin_unittest_user()
    delete_player_unittest_user()
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(a_device_id)
    delete_unittest_device(p_device_id)

    # validation
    assert response.status_code == 200
    assert response.get_json()['get_status'] == True

def test_admin_change_booking_status_approved():
    # Player prerequirements
    insert_player_unittest_user()
    p_device_id = newVirtualDeviceID()
    p_token = newUserToken()
    insert_unittest_device(p_device_id)
    insert_player_unittest_token(p_token, p_device_id)

    # Admin prerequirements
    insert_admin_unittest_user()
    a_device_id = newVirtualDeviceID()
    insert_unittest_device(a_device_id)
    a_token = newUserToken()
    insert_admin_unittest_token(a_token, a_device_id)
    venue_id = newSportFieldUUID()
    sport_kind_id = insert_admin_unittest_sport_kind()
    insert_admin_unittest_sport_venue(venue_id, sport_kind_id)
    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, venue_id, 1)

    # Conditiion prerequirements
    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2025-03-26", "13:00:00", "14:59:59")

    # test
    header = {
        'token': a_token
    }

    body = {
        'reservation_id': booking_id,
        'status': 'approved'
    }

    url = f"/admin/reservation/status"

    client = app.test_client()

    response = client.put(url, headers=header, json=body)

    # clean
    delete_admin_unittest_user()
    delete_player_unittest_user()
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(a_device_id)
    delete_unittest_device(p_device_id)

    # validation
    assert response.status_code == 200
    assert response.get_json()['edit_status'] == True

def test_admin_change_booking_status_rejected():
    # Player prerequirements
    insert_player_unittest_user()
    p_device_id = newVirtualDeviceID()
    p_token = newUserToken()
    insert_unittest_device(p_device_id)
    insert_player_unittest_token(p_token, p_device_id)

    # Admin prerequirements
    insert_admin_unittest_user()
    a_device_id = newVirtualDeviceID()
    insert_unittest_device(a_device_id)
    a_token = newUserToken()
    insert_admin_unittest_token(a_token, a_device_id)
    venue_id = newSportFieldUUID()
    sport_kind_id = insert_admin_unittest_sport_kind()
    insert_admin_unittest_sport_venue(venue_id, sport_kind_id)
    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, venue_id, 1)

    # Conditiion prerequirements
    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2025-03-26", "13:00:00", "14:59:59")

    # test
    header = {
        'token': a_token
    }

    body = {
        'reservation_id': booking_id,
        'status': 'rejected'
    }

    url = f"/admin/reservation/status"

    client = app.test_client()

    response = client.put(url, headers=header, json=body)

    # clean
    delete_admin_unittest_user()
    delete_player_unittest_user()
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(a_device_id)
    delete_unittest_device(p_device_id)

    # validation
    assert response.status_code == 200
    assert response.get_json()['edit_status'] == True

def test_admin_change_booking_status_cancelled():
    # Player prerequirements
    insert_player_unittest_user()
    p_device_id = newVirtualDeviceID()
    p_token = newUserToken()
    insert_unittest_device(p_device_id)
    insert_player_unittest_token(p_token, p_device_id)

    # Admin prerequirements
    insert_admin_unittest_user()
    a_device_id = newVirtualDeviceID()
    insert_unittest_device(a_device_id)
    a_token = newUserToken()
    insert_admin_unittest_token(a_token, a_device_id)
    venue_id = newSportFieldUUID()
    sport_kind_id = insert_admin_unittest_sport_kind()
    insert_admin_unittest_sport_venue(venue_id, sport_kind_id)
    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, venue_id, 1)

    # Conditiion prerequirements
    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2025-03-26", "13:00:00", "14:59:59")

    # test
    header = {
        'token': a_token
    }

    body = {
        'reservation_id': booking_id,
        'status': 'cancelled'
    }

    url = f"/admin/reservation/status"

    client = app.test_client()

    response = client.put(url, headers=header, json=body)

    # clean
    delete_admin_unittest_user()
    delete_player_unittest_user()
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(a_device_id)
    delete_unittest_device(p_device_id)

    # validation
    assert response.status_code == 200
    assert response.get_json()['edit_status'] == True

def test_admin_change_booking_status_waiting_approval():
    # Player prerequirements
    insert_player_unittest_user()
    p_device_id = newVirtualDeviceID()
    p_token = newUserToken()
    insert_unittest_device(p_device_id)
    insert_player_unittest_token(p_token, p_device_id)

    # Admin prerequirements
    insert_admin_unittest_user()
    a_device_id = newVirtualDeviceID()
    insert_unittest_device(a_device_id)
    a_token = newUserToken()
    insert_admin_unittest_token(a_token, a_device_id)
    venue_id = newSportFieldUUID()
    sport_kind_id = insert_admin_unittest_sport_kind()
    insert_admin_unittest_sport_venue(venue_id, sport_kind_id)
    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, venue_id, 1)

    # Conditiion prerequirements
    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2025-03-26", "13:00:00", "14:59:59")

    # test
    header = {
        'token': a_token
    }

    body = {
        'reservation_id': booking_id,
        'status': 'waiting_approval'
    }

    url = f"/admin/reservation/status"

    client = app.test_client()

    response = client.put(url, headers=header, json=body)

    # clean
    delete_admin_unittest_user()
    delete_player_unittest_user()
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(a_device_id)
    delete_unittest_device(p_device_id)

    # validation
    assert response.status_code == 200
    assert response.get_json()['edit_status'] == True

def test_admin_change_booking_status_not_valid():
    # Player prerequirements
    insert_player_unittest_user()
    p_device_id = newVirtualDeviceID()
    p_token = newUserToken()
    insert_unittest_device(p_device_id)
    insert_player_unittest_token(p_token, p_device_id)

    # Admin prerequirements
    insert_admin_unittest_user()
    a_device_id = newVirtualDeviceID()
    insert_unittest_device(a_device_id)
    a_token = newUserToken()
    insert_admin_unittest_token(a_token, a_device_id)
    venue_id = newSportFieldUUID()
    sport_kind_id = insert_admin_unittest_sport_kind()
    insert_admin_unittest_sport_venue(venue_id, sport_kind_id)
    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, venue_id, 1)

    # Conditiion prerequirements
    booking_id = newBookingUUID()
    insert_booking_unittest(booking_id, field_id, "2025-03-26", "13:00:00", "14:59:59")

    # test
    header = {
        'token': a_token
    }

    body = {
        'reservation_id': booking_id,
        'status': 'not_valid_stat'
    }

    url = f"/admin/reservation/status"

    client = app.test_client()

    response = client.put(url, headers=header, json=body)

    # clean
    delete_admin_unittest_user()
    delete_player_unittest_user()
    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(a_device_id)
    delete_unittest_device(p_device_id)

    # validation
    assert response.status_code == 400
    assert response.get_json()['edit_status'] == False
