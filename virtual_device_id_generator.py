import random
import pymysql
from db_config import mysql

def generateID():
    return ''.join(random.SystemRandom().choice(
        [chr(i) for i in range(97, 123)] +
        [str(i) for i in range(10)] +
        [chr(i) for i in range(65, 91)] +
        [chr(i) for i in range(40, 64)]) for _ in range(32)
    )

def getDeviceIDList():
    """function to get list of existing device ids"""
    query = 'SELECT id FROM Virtual_Device_ID'
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    read_row = cursor.fetchall()
    cursor.close()
    conn.close()
    return read_row

def newVirtualDeviceID():
    """generate new virtual device id that doesn't exist in DB"""
    list_ID = getDeviceIDList()
    new_ID = generateID()
    i = 0
    found = False
    while found == False and i < len(list_ID):
        if new_ID == list_ID[i]['id']:
            found = True
        i += 1

    ## recursion
    if found == False:
        return new_ID
    else:
        return newVirtualDeviceID()