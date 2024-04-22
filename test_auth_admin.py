from db_config import mysql
import pymysql
from app import app
from dotenv import load_dotenv
load_dotenv()
import os
from token_generator import newUserToken
from virtual_device_id_generator import newVirtualDeviceID

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

### ============================ UNIT TEST ================================= ###

def test_auth_admin_register():
    """Testing register admin success"""
    client = app.test_client()
    url = '/admin/auth/register'

    mock_request_body = {
        "username": "unittest",
        "password": "unittest",
        "name": "Unit Test",
        "phone": "08123456789"
    }

    response = client.post(url, json=mock_request_body)

    query = 'DELETE FROM Admin WHERE username = "'+mock_request_body["username"]+'"'
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

    assert response.status_code == 200
    assert response.get_json()['register_status'] == True

def test_auth_admin_register_failed():
    """Testing register admin failed"""
    client = app.test_client()
    url = '/admin/auth/register'

    insert_unittest_user()

    mock_request_body = {
        "username": "unittest",
        "password": "unittest",
        "name": "Unit Test",
        "phone": "08123456789"
    }

    response = client.post(url, json=mock_request_body)

    delete_unittest_user()

    assert response.status_code == 409
    assert response.get_json()['register_status'] == False

def test_auth_admin_login_success():
    """Testing login admin success"""
    client = app.test_client()
    url = '/admin/auth/login'

    insert_unittest_user()
    device_id = newVirtualDeviceID()
    insert_unittest_device(device_id)

    mock_request_body = {
        "username": "unittest",
        "password": "unittest",
        "virtual_device_id": device_id
    }

    response = client.post(url, json=mock_request_body)

    delete_unittest_user()
    delete_unittest_device(device_id)

    assert response.status_code == 200
    assert response.get_json()['login_status'] == True

def test_auth_admin_login_username_not_found():
    """Testing login admin username not found"""
    client = app.test_client()
    url = '/admin/auth/login'

    device_id = newVirtualDeviceID()
    insert_unittest_device(device_id)

    mock_request_body = {
        "username": "unittest",
        "password": "unittest",
        "virtual_device_id": device_id
    }

    response = client.post(url, json=mock_request_body)

    delete_unittest_user()
    delete_unittest_device(device_id)

    assert response.status_code == 404
    assert response.get_json()['login_status'] == False
    assert response.get_json()['message'] == "Username not found"

def test_auth_admin_login_password_wrong():
    """Testing login admin password wrong"""
    client = app.test_client()
    url = '/admin/auth/login'

    insert_unittest_user()
    device_id = newVirtualDeviceID()
    insert_unittest_device(device_id)

    mock_request_body = {
        "username": "unittest",
        "password": "wrongpassword",
        "virtual_device_id": device_id
    }

    response = client.post(url, json=mock_request_body)

    delete_unittest_user()
    delete_unittest_device(device_id)

    assert response.status_code == 400
    assert response.get_json()['login_status'] == False
    assert response.get_json()['message'] == "Password doesn't match"

def test_auth_admin_relogin_token_valid():
    """Testing relogin with valid token"""
    client = app.test_client()
    url = '/auth/relogin'

    token = newUserToken()
    insert_unittest_user()
    device_id = newVirtualDeviceID()
    insert_unittest_device(device_id)
    insert_unittest_token(token, device_id)
    header = {
        "token": token
    }
    response = client.get(url, headers=header)

    delete_unittest_user()
    delete_unittest_device(device_id)

    assert response.status_code == 200
    assert response.get_json()['relogin_status'] == True
    assert response.get_json()['message'] == "Token is valid, relogin successfully"
    assert response.get_json()['data']['username'] == "unittest"
    assert response.get_json()['data']['role'] == "admin"

def test_auth_admin_relogin_token_invalid():
    """Testing relogin with invalid token"""
    client = app.test_client()
    url = '/auth/relogin'

    token = newUserToken()
    insert_unittest_user()
    device_id = newVirtualDeviceID()
    insert_unittest_device(device_id)
    insert_unittest_token(token, device_id)
    header = {
        "token": newUserToken()
    }
    response = client.get(url, headers=header)

    delete_unittest_user()
    delete_unittest_device(device_id)

    assert response.status_code == 400
    assert response.get_json()['relogin_status'] == False
    assert response.get_json()['message'] == "Token is already expired"
    assert response.get_json()['data']['username'] == None

def test_auth_admin_logout():
    """Testing logout admin"""
    client = app.test_client()
    url = '/admin/auth/logout'

    device_id = newVirtualDeviceID()
    insert_unittest_device(device_id)
    insert_unittest_user()
    token = newUserToken()
    insert_unittest_token(token, device_id)

    header = {
        "token": token
    }
    response = client.delete(url, headers=header)

    delete_unittest_user()
    delete_unittest_device(device_id)

    assert response.status_code == 200
    assert response.get_json()['logout_status'] == True
    assert response.get_json()['message'] == "Logout user in this device is successfully"
