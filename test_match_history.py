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

def test_create_match_history_by_host_number_exists():
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
    insert_new_match_history_custom(reservation_id, newMatchHistoryUUID(), 1)

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
    assert response.status_code == 409
    assert response.get_json()['status'] == False
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

    # test
    url = f"/player/reservation/match-history/{reservation_id}"
    client = app.test_client()
    response = client.get(url, headers=header)

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

    # test
    url = f"/player/reservation/match-history/{reservation_id}"
    client = app.test_client()
    response = client.get(url, headers=header)

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

def test_delete_match_history_by_host_or_member():
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
    match_id = newMatchHistoryUUID()
    insert_new_match_history_custom(reservation_id, match_id, 1)

    header = {
        'token': token_player
    }
    body = {
        'reservation_id': reservation_id,
        'match_history_id': match_id
    }

    # test
    url = f"/player/reservation/match-history"
    client = app.test_client()
    response = client.delete(url, headers=header, json=body)

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

def test_edit_number_match_history_by_host_or_member_not_exists():
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
    match_id = newMatchHistoryUUID()
    insert_new_match_history_custom(reservation_id, match_id, 1)

    header = {
        'token': token_player
    }
    body = {
        'reservation_id': reservation_id,
        'match_history_id': match_id,
        'new_number': 2
    }

    # test
    url = f"/player/reservation/match-history"
    client = app.test_client()
    response = client.put(url, headers=header, json=body)

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


def test_edit_number_match_history_by_host_or_member_exists():
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
    match_id = newMatchHistoryUUID()
    insert_new_match_history_custom(reservation_id, match_id, 1)
    match_id_2 = newMatchHistoryUUID()
    insert_new_match_history_custom(reservation_id, match_id_2, 2)

    header = {
        'token': token_player
    }
    body = {
        'reservation_id': reservation_id,
        'match_history_id': match_id_2,
        'new_number': 1
    }

    # test
    url = f"/player/reservation/match-history"
    client = app.test_client()
    response = client.put(url, headers=header, json=body)

    # clean test data
    delete_admin_unittest_user()
    delete_player_unittest_user()
    delete_unittest_device(device_admin)
    delete_unittest_device(device_player)
    delete_admin_unittest_sport_kind(sport_kind_id)

    # assertion
    assert response.status_code == 409
    assert response.get_json()['status'] == False
    assert response.get_json()['data'] == None

def test_edit_score_match_history_by_host_or_member():
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
    match_id = newMatchHistoryUUID()
    insert_new_match_history_custom(reservation_id, match_id, 1)

    header = {
        'token': token_player
    }
    body = {
        'reservation_id': reservation_id,
        'match_history_id': match_id,
        'score_a': 21,
        'score_b': 18
    }

    # test
    url = f"/player/reservation/match-history/score"
    client = app.test_client()
    response = client.put(url, headers=header, json=body)

    query = f"SELECT score_a, score_b FROM Match_History WHERE id = '{match_id}'"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    conn.close()

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
    assert result['score_a'] == body['score_a']
    assert result['score_b'] == body['score_b']

def test_edit_score_match_history_by_host_or_member_2():
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
    match_id = newMatchHistoryUUID()
    insert_new_match_history_custom(reservation_id, match_id, 1)

    header = {
        'token': token_player
    }
    body = {
        'reservation_id': reservation_id,
        'match_history_id': match_id,
        'score_a': 3,
        'score_b': 21
    }

    # test
    url = f"/player/reservation/match-history/score"
    client = app.test_client()
    response = client.put(url, headers=header, json=body)

    query = f"SELECT score_a, score_b FROM Match_History WHERE id = '{match_id}'"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    conn.close()

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
    assert result['score_a'] == body['score_a']
    assert result['score_b'] == body['score_b']

def test_insert_player_to_a_match_history_valid_member():
    # preparation
    username_admin = 'unittest'
    username_player = 'unittest'
    username_player_member = 'unittest_pm'
    insert_admin_unittest_user_custom(username_admin)
    insert_player_unittest_user_custom(username_player)
    insert_player_unittest_user_custom(username_player_member)

    sport_kind_id = insert_admin_unittest_sport_kind()

    venue_id = newSportFieldUUID()
    insert_admin_unittest_sport_venue(venue_id, sport_kind_id)
    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, venue_id, 1)

    reservation_id = newBookingUUID()
    insert_booking_unittest(reservation_id, field_id, '2024-06-12', '09:00:00', '11:00:00')
    change_reservation_status(reservation_id, 'approved')
    insert_member_reservation(reservation_id, username_player_member)

    device_pm = newVirtualDeviceID()
    insert_unittest_device(device_pm)
    token_pm = newUserToken()
    insert_player_unittest_token_custom(token_pm, device_pm, username_player_member)
    match_id = newMatchHistoryUUID()
    insert_new_match_history_custom(reservation_id, match_id, 1)

    # condition
    header = {
        'token': token_pm
    }
    body = {
        'reservation_id': reservation_id,
        'match_history_id': match_id,
        'username': username_player_member,
        'team': 'a'
    }

    # test
    url = "/player/reservation/match-history/player"
    client = app.test_client()
    response = client.post(url, headers=header, json=body)

    # cleaning
    delete_admin_unittest_user_custom(username_admin)
    delete_player_unittest_user_custom(username_player)
    delete_player_unittest_user_custom(username_player_member)

    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_pm)

    # assert
    assert response.status_code == 200
    assert response.get_json()['status'] == True
    assert response.get_json()['data'] != None

def test_insert_player_to_a_match_history_valid_host():
    # preparation
    username_admin = 'unittest'
    username_player = 'unittest'
    username_player_member = 'unittest_pm'
    insert_admin_unittest_user_custom(username_admin)
    insert_player_unittest_user_custom(username_player)
    insert_player_unittest_user_custom(username_player_member)

    sport_kind_id = insert_admin_unittest_sport_kind()
    venue_id = newSportFieldUUID()
    insert_admin_unittest_sport_venue(venue_id, sport_kind_id)
    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, venue_id, 1)

    reservation_id = newBookingUUID()
    insert_booking_unittest(reservation_id, field_id, '2024-06-12', '09:00:00', '11:00:00')
    change_reservation_status(reservation_id, 'approved')
    insert_member_reservation(reservation_id, username_player_member)

    device_pm = newVirtualDeviceID()
    insert_unittest_device(device_pm)
    token_pm = newUserToken()
    insert_player_unittest_token_custom(token_pm, device_pm, username_player_member)
    match_id = newMatchHistoryUUID()
    insert_new_match_history_custom(reservation_id, match_id, 1)

    # condition
    header = {
        'token': token_pm
    }
    body = {
        'reservation_id': reservation_id,
        'match_history_id': match_id,
        'username': 'unittest',
        'team': 'a'
    }

    # test
    url = "/player/reservation/match-history/player"
    client = app.test_client()
    response = client.post(url, headers=header, json=body)

    # cleaning
    delete_admin_unittest_user_custom(username_admin)
    delete_player_unittest_user_custom(username_player)
    delete_player_unittest_user_custom(username_player_member)

    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_pm)

    # assert
    assert response.status_code == 200
    assert response.get_json()['status'] == True
    assert response.get_json()['data'] != None

def test_insert_player_to_a_match_history_invalid_member_or_host():
    # preparation
    username_admin = 'unittest'
    username_player = 'unittest'
    username_player_member = 'unittest_pm'
    username_player_invalid = 'unittest_invalid'
    insert_admin_unittest_user_custom(username_admin)
    insert_player_unittest_user_custom(username_player)
    insert_player_unittest_user_custom(username_player_member)
    insert_player_unittest_user_custom(username_player_invalid)

    sport_kind_id = insert_admin_unittest_sport_kind()
    venue_id = newSportFieldUUID()
    insert_admin_unittest_sport_venue(venue_id, sport_kind_id)
    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, venue_id, 1)

    reservation_id = newBookingUUID()
    insert_booking_unittest(reservation_id, field_id, '2024-06-12', '09:00:00', '11:00:00')
    change_reservation_status(reservation_id, 'approved')
    insert_member_reservation(reservation_id, username_player_member)

    device_pm = newVirtualDeviceID()
    insert_unittest_device(device_pm)
    token_pm = newUserToken()
    insert_player_unittest_token_custom(token_pm, device_pm, username_player_member)
    match_id = newMatchHistoryUUID()
    insert_new_match_history_custom(reservation_id, match_id, 1)

    # condition
    header = {
        'token': token_pm
    }
    body = {
        'reservation_id': reservation_id,
        'match_history_id': match_id,
        'username': username_player_invalid,
        'team': 'a'
    }

    # test
    url = "/player/reservation/match-history/player"
    client = app.test_client()
    response = client.post(url, headers=header, json=body)

    # cleaning
    delete_admin_unittest_user_custom(username_admin)
    delete_player_unittest_user_custom(username_player)
    delete_player_unittest_user_custom(username_player_member)
    delete_player_unittest_user_custom(username_player_invalid)

    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_pm)

    # assert
    assert response.status_code == 403
    assert response.get_json()['status'] == False
    assert response.get_json()['message'] == 'Only host or member that could added to a match history'
    assert response.get_json()['data'] == None

def test_insert_player_to_a_match_history_user_already_in_a_match():
    # preparation
    username_admin = 'unittest'
    username_player = 'unittest'
    username_player_member = 'unittest_pm'
    insert_admin_unittest_user_custom(username_admin)
    insert_player_unittest_user_custom(username_player)
    insert_player_unittest_user_custom(username_player_member)

    sport_kind_id = insert_admin_unittest_sport_kind()
    venue_id = newSportFieldUUID()
    insert_admin_unittest_sport_venue(venue_id, sport_kind_id)
    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, venue_id, 1)

    reservation_id = newBookingUUID()
    insert_booking_unittest(reservation_id, field_id, '2024-06-12', '09:00:00', '11:00:00')
    change_reservation_status(reservation_id, 'approved')
    insert_member_reservation(reservation_id, username_player_member)

    device_pm = newVirtualDeviceID()
    insert_unittest_device(device_pm)
    token_pm = newUserToken()
    insert_player_unittest_token_custom(token_pm, device_pm, username_player_member)
    match_id = newMatchHistoryUUID()
    insert_new_match_history_custom(reservation_id, match_id, 1)
    insert_match_player(match_id, 'unittest', 'a')

    # condition
    header = {
        'token': token_pm
    }
    body = {
        'reservation_id': reservation_id,
        'match_history_id': match_id,
        'username': 'unittest',
        'team': 'a'
    }

    # test
    url = "/player/reservation/match-history/player"
    client = app.test_client()
    response = client.post(url, headers=header, json=body)

    # cleaning
    delete_admin_unittest_user_custom(username_admin)
    delete_player_unittest_user_custom(username_player)
    delete_player_unittest_user_custom(username_player_member)

    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_pm)

    # assert
    assert response.status_code == 409
    assert response.get_json()['status'] == False
    assert response.get_json()['message'] == f"unittest is already in this match history"
    assert response.get_json()['data'] == None

def test_insert_player_to_a_match_history_user_already_in_a_match():
    # preparation
    username_admin = 'unittest'
    username_player = 'unittest'
    username_player_member = 'unittest_pm'
    insert_admin_unittest_user_custom(username_admin)
    insert_player_unittest_user_custom(username_player)
    insert_player_unittest_user_custom(username_player_member)

    sport_kind_id = insert_admin_unittest_sport_kind()
    venue_id = newSportFieldUUID()
    insert_admin_unittest_sport_venue(venue_id, sport_kind_id)
    field_id = newFieldUUID()
    insert_admin_unittest_field_to_venue(field_id, venue_id, 1)

    reservation_id = newBookingUUID()
    insert_booking_unittest(reservation_id, field_id, '2024-06-12', '09:00:00', '11:00:00')
    change_reservation_status(reservation_id, 'waiting_approval')
    insert_member_reservation(reservation_id, username_player_member)

    device_pm = newVirtualDeviceID()
    insert_unittest_device(device_pm)
    token_pm = newUserToken()
    insert_player_unittest_token_custom(token_pm, device_pm, username_player_member)
    match_id = newMatchHistoryUUID()
    insert_new_match_history_custom(reservation_id, match_id, 1)

    # condition
    header = {
        'token': token_pm
    }
    body = {
        'reservation_id': reservation_id,
        'match_history_id': match_id,
        'username': 'unittest',
        'team': 'a'
    }

    # test
    url = "/player/reservation/match-history/player"
    client = app.test_client()
    response = client.post(url, headers=header, json=body)

    # cleaning
    delete_admin_unittest_user_custom(username_admin)
    delete_player_unittest_user_custom(username_player)
    delete_player_unittest_user_custom(username_player_member)

    delete_admin_unittest_sport_kind(sport_kind_id)
    delete_unittest_device(device_pm)

    # assert
    assert response.status_code == 403
    assert response.get_json()['status'] == False
    assert response.get_json()['message'] == f"Reservation is not approved by admin"
    assert response.get_json()['data'] == None
