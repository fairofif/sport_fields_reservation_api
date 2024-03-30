import pymysql
from flask import (
    jsonify,
    request
)
from db_config import mysql
from virtual_device_id_generator import newVirtualDeviceID
from dotenv import load_dotenv
load_dotenv(override=True)

def device_configure_routes(app):
    @app.route('/device/register', methods=['POST'])
    def register_device():
        device_id = newVirtualDeviceID()
        query = "INSERT INTO Virtual_Device_ID VALUES ('"+device_id+"', CURRENT_TIMESTAMP())"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()

        response = {
            "register_status": True,
            "message": "Register device successfully",
            "data": {
                "virtual_device_id": device_id
            }
        }
        return jsonify(response)

    @app.route('/device/delete', methods=['DELETE'])
    def delete_device():
        body = request.json
        device_id = body['virtual_device_id']
        query = "DELETE FROM Virtual_Device_ID WHERE id = '"+device_id+"'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()

        response = {
            "delete_status": True,
            "message": "This device has been deleted from register app"
        }

        return jsonify(response)