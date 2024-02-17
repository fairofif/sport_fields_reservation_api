from flask import jsonify
import json
from db_config import mysql
import pymysql
from app import app
from dotenv import load_dotenv
load_dotenv()
import os
from token_generator import newPlayerToken

# ============================= Local Function ==============================

def insert_unittest_user():
    ava_url = os.getenv("DEFAULT_AVA_PATH")

    query = 'INSERT INTO Player VALUES("unittest", "unittest", "Unit Test", "'+ava_url+'", CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP)'
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def delete_unittest_user():
    query = 'DELETE FROM Player WHERE username = "unittest"'
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def delete_unittest_token():
    query = "DELETE FROM Player_Login_Token WHERE Player_username = 'unittest'"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def insert_unittest_token(token):
    query = "INSERT INTO Player_Login_Token VALUES ('"+token+"', 'unittest', CURRENT_TIMESTAMP)"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

# ============================= UNIT TEST ===================================

def test_auth_player_register():
    """Testing register player success"""
    client = app.test_client()
    url = '/player/auth/register'

    mock_request_body = {
        "username": "unittest",
        "password": "unittest",
        "name": "Unit Test"
    }

    response = client.post(url, json=mock_request_body)

    query = 'DELETE FROM Player WHERE username = "'+mock_request_body["username"]+'"'
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

    assert response.status_code == 200
    assert response.get_json()['register_status'] == True

def test_auth_player_register_failed():
    """Testing register player failed"""
    client = app.test_client()
    url = '/player/auth/register'

    insert_unittest_user()

    mock_request_body = {
        "username": "unittest",
        "password": "unittest",
        "name": "Unit Test"
    }

    response = client.post(url, json=mock_request_body)

    delete_unittest_token()
    delete_unittest_user()

    assert response.status_code == 200
    assert response.get_json()['register_status'] == False

def test_auth_player_login_success():
    """Testing login player success"""
    client = app.test_client()
    url = '/player/auth/login'

    insert_unittest_user()

    mock_request_body = {
        "username": "unittest",
        "password": "unittest"
    }

    response = client.post(url, json=mock_request_body)

    delete_unittest_user()

    assert response.status_code == 200
    assert response.get_json()['login_status'] == True

def test_auth_player_login_username_not_found():
    """Testing login player username not found"""
    client = app.test_client()
    url = '/player/auth/login'

    mock_request_body = {
        "username": "unittest",
        "password": "unittest"
    }

    response = client.post(url, json=mock_request_body)

    delete_unittest_user()

    assert response.status_code == 200
    assert response.get_json()['login_status'] == False
    assert response.get_json()['message'] == "Username not found"

def test_auth_player_login_password_wrong():
    """Testing login player password wrong"""
    client = app.test_client()
    url = '/player/auth/login'

    insert_unittest_user()

    mock_request_body = {
        "username": "unittest",
        "password": "wrongpassword"
    }

    response = client.post(url, json=mock_request_body)

    delete_unittest_user()

    assert response.status_code == 200
    assert response.get_json()['login_status'] == False
    assert response.get_json()['message'] == "Password doesn't match"

def test_auth_player_relogin_token_valid():
    """Testing relogin with valid token"""
    client = app.test_client()
    url = '/player/auth/relogin'

    token = newPlayerToken()
    insert_unittest_user()
    insert_unittest_token(token)
    header = {
        "token": token
    }
    response = client.get(url, headers=header)

    delete_unittest_user()

    assert response.status_code == 200
    assert response.get_json()['relogin_status'] == True
    assert response.get_json()['message'] == "Token is valid, relogin successfully"
    assert response.get_json()['username'] == "unittest"

def test_auth_player_relogin_token_invalid():
    """Testing relogin with invalid token"""
    client = app.test_client()
    url = '/player/auth/relogin'

    token = newPlayerToken()
    insert_unittest_user()
    insert_unittest_token(token)
    header = {
        "token": newPlayerToken()
    }
    response = client.get(url, headers=header)

    delete_unittest_user()

    assert response.status_code == 200
    assert response.get_json()['relogin_status'] == False
    assert response.get_json()['message'] == "Token is already expired"
    assert response.get_json()['username'] == "NULL"
