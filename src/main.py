#!/usr/bin/env python3
from flask import Flask
import pymysql
import time
import os

environment = os.getenv("APP_ENVIRONMENT", "local")

if environment == "local":
    hostname = "localhost"
else: 
    hostname = "mysql"

con = None
def open_db_connection() -> None:
    retry = 0   
    while retry <=5:
        try:
            global con
            con = pymysql.connect(host=hostname, user="admin", passwd="admin", db="main" )
            break
        except Exception as error:
            print(error)
            retry += 1
            time.sleep(retry*5)
    
    if retry == 6:
        raise ValueError(f"Db connection failed after max retry: {retry}")


# Simple routine to run a query on a database and print the results:
def sql(conn, query) :
    cur = conn.cursor()
    cur.execute(query)
    for id, lastname in cur.fetchall() :

        return {id:lastname}

api = Flask(__name__)

@api.route('/')
def index():
    query = "SELECT * FROM Persons"
    return repr(sql(con,query))



if __name__ == '__main__':
    open_db_connection()
    api.run(debug=True, host='0.0.0.0')
    con.close()