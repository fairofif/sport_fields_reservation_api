from flask import jsonify
import json

from app import app

def test_base_route():
    client = app.test_client()
    url = '/'
    response = client.get(url)
    assert response.status_code == 200
    assert response.get_json()['data'] == "Hello"

def test_base_route2():
    client = app.test_client()
    url = '/test'
    response = client.get(url)
    assert response.status_code == 200
    assert response.get_json()['data'] == "Hello"

def test_login():
    client = app.test_client()
    url = '/login'

    mock_request_body = {
        'username': 'devexample',
        'password': 'examplepass'
    }

    response = client.post(url, json=mock_request_body)
    assert response.status_code == 200
    assert response.get_json()["message"] == "Login Success"

def test_swagger_success():
    client = app.test_client()
    url = '/api/docs/#/'
    response = client.get(url)
    assert response.status_code == 200