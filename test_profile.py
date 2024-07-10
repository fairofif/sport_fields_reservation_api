from app import app
from static import *

def test_get_user_public_information_admin():
    # preparation
    username_admin = 'unittest'
    insert_admin_unittest_user_custom(username_admin)

    username_player = 'unittest_p'
    insert_player_unittest_user_custom(username_player)
    device_player = newVirtualDeviceID()
    insert_unittest_device(device_player)
    token_player = newUserToken()
    insert_player_unittest_token_custom(token_player, device_player, username_player)

    # test
    header = {
        'token': token_player
    }
    url = f"/user-info/{username_admin}"
    client = app.test_client()

    response = client.get(url, headers=header)

    # cleaning
    delete_admin_unittest_user_custom(username_admin)
    delete_unittest_device(device_player)
    delete_player_unittest_user_custom(username_player)

    # assertion
    assert response.status_code == 200
    assert response.get_json()['status'] == True
    assert response.get_json()['data'] != None
    assert response.get_json()['data']['role'] == 'admin'

def test_get_user_public_information_player():
    # preparation
    username_admin = 'unittest_a'
    insert_admin_unittest_user_custom(username_admin)

    username_player = 'unittest_p'
    insert_player_unittest_user_custom(username_player)

    device_admin = newVirtualDeviceID()
    insert_unittest_device(device_admin)
    token_admin = newUserToken()
    insert_admin_unittest_token_custom(token_admin, device_admin, username_admin)

    # test
    header = {
        'token': token_admin
    }
    url = f"/user-info/{username_player}"
    client = app.test_client()

    response = client.get(url, headers=header)

    # cleaning
    delete_admin_unittest_user_custom(username_admin)
    delete_unittest_device(device_admin)
    delete_player_unittest_user_custom(username_player)

    # assertion
    assert response.status_code == 200
    assert response.get_json()['status'] == True
    assert response.get_json()['data'] != None
    assert response.get_json()['data']['role'] == 'player'

def test_get_user_public_information_username_not_found():
    # preparation
    username_admin = 'unittest_a'
    insert_admin_unittest_user_custom(username_admin)

    username_player = 'unittest_p'
    insert_player_unittest_user_custom(username_player)

    device_admin = newVirtualDeviceID()
    insert_unittest_device(device_admin)
    token_admin = newUserToken()
    insert_admin_unittest_token_custom(token_admin, device_admin, username_admin)

    # test
    header = {
        'token': token_admin
    }
    url = f"/user-info/gg8ah5aib4ewdu1n"
    client = app.test_client()

    response = client.get(url, headers=header)

    # cleaning
    delete_admin_unittest_user_custom(username_admin)
    delete_unittest_device(device_admin)
    delete_player_unittest_user_custom(username_player)

    # assertion
    assert response.status_code == 404
    assert response.get_json()['status'] == False
    assert response.get_json()['data'] == None

def test_edit_user_information_valid():
    # preparation
    username_player = 'unittest_p'
    insert_player_unittest_user_custom(username_player)

    device_player = newVirtualDeviceID()
    insert_unittest_device(device_player)
    token_player = newUserToken()
    insert_player_unittest_token_custom(token_player, device_player, username_player)

    # condition
    username_player_change = 'unittest_edit_p'

    header = {
        'token': token_player
    }

    body = {
        'username': username_player_change,
        'name': 'Nama Baru',
        'phone': '08122931323'
    }

    # test client
    url = '/user-info'

    client = app.test_client()
    response = client.put(url, headers=header, json=body)

    # cleaning
    delete_player_unittest_user_custom(username_player_change)
    delete_player_unittest_user_custom(username_player)
    delete_unittest_device(device_player)

    # assert
    assert response.status_code == 200
    assert response.get_json()['data']['username'] == username_player_change

def test_edit_user_information_username_exists():
    # preparation
    username_player = 'unittest_p'
    insert_player_unittest_user_custom(username_player)
    username_player_2 = 'unittest_p_2'
    insert_player_unittest_user_custom(username_player_2)

    device_player = newVirtualDeviceID()
    insert_unittest_device(device_player)
    token_player = newUserToken()
    insert_player_unittest_token_custom(token_player, device_player, username_player)

    # condition
    header = {
        'token': token_player
    }

    body = {
        'username': username_player_2,
        'name': 'Nama Baru',
        'phone': None
    }

    # test client
    url = '/user-info'

    client = app.test_client()
    response = client.put(url, headers=header, json=body)

    # cleaning
    delete_player_unittest_user_custom(username_player_2)
    delete_player_unittest_user_custom(username_player)
    delete_unittest_device(device_player)

    # assert
    assert response.status_code == 409
    assert response.get_json()['message'] == f"username {username_player_2} is exists"

def test_edit_user_information_valid_only_not_sensitive_content():
    # preparation
    username_player = 'unittest_p'
    insert_player_unittest_user_custom(username_player)

    device_player = newVirtualDeviceID()
    insert_unittest_device(device_player)
    token_player = newUserToken()
    insert_player_unittest_token_custom(token_player, device_player, username_player)

    # condition
    header = {
        'token': token_player
    }

    body = {
        'username': None,
        'name': 'Nama Baru',
        'phone': '08122931323'
    }

    # test client
    url = '/user-info'

    client = app.test_client()
    response = client.put(url, headers=header, json=body)

    # cleaning
    delete_player_unittest_user_custom(username_player)
    delete_unittest_device(device_player)

    # assert
    assert response.status_code == 200
    assert response.get_json()['data']['name'] == 'Nama Baru'
