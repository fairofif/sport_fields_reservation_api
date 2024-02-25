import uuid
import pymysql
from db_config import mysql

def newSportKindUUID():
    query = "SELECT * FROM Sport_Kind"
    conn = mysql.connect()
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    read_row = cursor.fetchall()
    cursor.close()
    conn.close()

    newUUID = str(uuid.uuid4())

    i = 0
    found = False
    while found == False and i < len(read_row):
        if read_row[i]['id'] == newUUID:
            found = True
        i += 1

    if found == False:
        return newUUID
    else:
        return newSportKindUUID()

def newSportFieldUUID():
    query = "SELECT * FROM Sport_Field"
    conn = mysql.connect()
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    read_row = cursor.fetchall()
    cursor.close()
    conn.close()

    newUUID = str(uuid.uuid4())

    i = 0
    found = False
    while found == False and i < len(read_row):
        if read_row[i]['id'] == newUUID:
            found = True
        i += 1

    if found == False:
        return newUUID
    else:
        return newSportFieldUUID()
