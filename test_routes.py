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
