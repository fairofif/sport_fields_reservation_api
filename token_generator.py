import random
import pymysql
from db_config import mysql

def generateToken():
    """function to generate random token"""
    return ''.join(random.SystemRandom().choice(
        [chr(i) for i in range(97, 123)] +
        [str(i) for i in range(10)] +
        [chr(i) for i in range(65, 91)] +
        [chr(i) for i in range(40, 64)]) for _ in range(128)
    )

def getPlayerTokenList():
    """function to get list of existing player token in DB"""
    query = 'SELECT token FROM Player_Login_Token'
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    read_row = cursor.fetchall()
    cursor.close()
    conn.close()
    return read_row

def getAdminTokenList():
    """function to get list of existing admin token in DB"""
    query = 'SELECT token FROM Admin_Login_Token'
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    read_row = cursor.fetchall()
    cursor.close()
    conn.close()
    return read_row

def newPlayerToken():
    """generate new player token that doesn't exist in DB"""
    listToken = getPlayerTokenList()
    new_token = generateToken()
    i = 0
    found = False
    while found == False and i < len(listToken):
        if new_token == listToken[i]['token']:
            found = True
        i += 1

    ## recursion
    if found == False:
        return new_token
    else:
        return newPlayerToken()

def newAdminToken():
    """generate new admin token that doesn't exist in DB"""
    listToken = getAdminTokenList()
    new_token = generateToken()
    i = 0
    found = False
    while found == False and i < len(listToken):
        if new_token == listToken[i]['token']:
            found = True
        i += 1

    ## recursion
    if found == False:
        return new_token
    else:
        return newAdminToken()
