#!/usr/bin/env python3
from flask import Flask, request
import pymysql
import time
import os
import json

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
    conn.commit()
    return cur

api = Flask(__name__)

@api.route('/')
def index():
    query = "SELECT * FROM Persons"
    response = sql(con,query)
    output = []
    for id, lastname in response.fetchall() :
        output.append({"id": id, "name": lastname})
    return json.dumps(output)

@api.route('/products', methods=['GET'])
def get_products():
    query = "SELECT * FROM Products"
    response = sql(con,query)
    output = []
    for id, lastname, price in response.fetchall() :
        output.append({"id": id, "name": lastname, "price":price})
    return json.dumps(output)

@api.route('/products', methods=['POST'])
def post_products():
    data = request.get_json(force=True)
    query = f"""INSERT INTO Products VALUES({data["id"]},'{data["name"]}', {data["price"]});"""
    sql(con,query)
    return f'Product successully added, query: {query}', 200 



if __name__ == '__main__':
    open_db_connection()
    api.run(debug=True, host='0.0.0.0')
    con.close()