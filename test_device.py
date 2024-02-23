from db_config import mysql
import pymysql
from app import app
from dotenv import load_dotenv
load_dotenv()
import os
from virtual_device_id_generator import newVirtualDeviceID

def insertUnitTestDevice(device_id):
    query = "INSERT INTO Virtual_Device_ID VALUES ('"+device_id+"', CURRENT_TIMESTAMP())"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def deleteUnitTestDevice(device_id):
    query = "DELETE FROM Virtual_Device_ID WHERE id = '"+device_id+"'"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

### ==================================== UNIT TEST =========================================== ###

def test_device_register():
    """Test register new device"""
    client = app.test_client()
    url = '/device/register'

    response = client.post(url)

    deleteUnitTestDevice(response.get_json()['virtual_device_id'])

    assert response.status_code == 200
    assert response.get_json()['virtual_device_id'] != None

def test_device_delete():
    """Test register delete device"""
    client = app.test_client()
    url = '/device/delete'

    device_id = newVirtualDeviceID()
    insertUnitTestDevice(device_id)

    body = {
        "virtual_device_id": device_id
    }

    response = client.delete(url, json=body)

    assert response.status_code == 200
    assert response.get_json()['delete_status'] == True
    assert response.get_json()['message'] == 'This device has been deleted from register app'