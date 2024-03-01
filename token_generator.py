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

def newUserToken():
    """generate new token unique both from admin and player"""
    list_token_admin = getAdminTokenList()
    list_token_player = getPlayerTokenList()
    list_all_token = list_token_admin + list_token_player

    new_token = generateToken()

    i = 0
    found = False
    while found == False and i < len(list_all_token):
        if new_token == list_all_token[i]['token']:
            found = True
        i += 1

    ## recursion
    if found == False:
        return new_token
    else:
        return newUserToken()

