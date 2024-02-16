from flask import jsonify
import json
from db_config import mysql
import pymysql
from app import app
from dotenv import load_dotenv
load_dotenv()
import os

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
    ava_url = os.getenv("DEFAULT_AVA_PATH")

    query = 'INSERT INTO Player VALUES("unittest", "unittest", "Unit Test", "'+ava_url+'", CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP)'
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

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
    assert response.get_json()['register_status'] == False
