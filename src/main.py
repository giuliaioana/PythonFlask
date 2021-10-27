#!/usr/bin/env python3
from flask import Flask, request
import pymysql
import time
import os
import json
import yaml
import sys
from flask_sqlalchemy import SQLAlchemy 
from config import settings
pymysql.install_as_MySQLdb()

api = Flask(__name__)

api.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{settings.user}:{settings.password}@{settings.hostname}/{settings.db}'
db = SQLAlchemy(api)

class Products(db.Model):
    __tablename__='Products'
    ProductID = db.Column(db.Integer,primary_key=True)
    ProductName = db.Column(db.String(64))
    Price = db.Column(db.Integer,nullable=False)
    #cartitems = db.relationship('Carts', backref='Products')
    def __repr__(self):
        return f'ProductName {self.ProductName}'

class Carts(db.Model):
    __tablename__='Carts'
    ID = db.Column(db.Integer,primary_key=True)
    PersonID = db.Column(db.Integer, db.ForeignKey('Persons.PersonID'))
    ProductID = db.Column(db.Integer, db.ForeignKey('Products.ProductID'))

class Persons(db.Model):
    __tablename__='Persons'
    PersonID = db.Column(db.Integer, primary_key=True)
    LastName = db.Column(db.String(64))

db.create_all()


# @api.route('/')

# def getproductitem():
#     itemid = products.id
#     productname = products.name
#     productname = Carts(product_id=itemid)
#     db.session.add(products)
#     db.session.commit()

@api.route('/persons')
def index():
    # query = "SELECT * FROM Persons"
    # response = sql(con,query)
    output = []
    for person in Persons.query.all():
        output.append({"id": person.PersonID, "name": person.LastName})
    # print(type(data))
    # print(*data)
    # # output = []
    # # for id, lastname in response.fetchall() :
    # #     output.append({"id": id, "name": lastname})
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


@api.route('/products/<int:id>', methods=['GET'])
def get_product_id(id):
   query = f"""SELECT * FROM Products WHERE ProductID={id};"""
   response = sql(con,query)
   output = []
   for id, lastname, price in response.fetchall() :
        output.append({"id": id, "name": lastname, "price":price})
   return json.dumps(output) 


@api.route('/products/<int:id>', methods=['PUT'])
def put_product_id(id):
   data = request.get_json(force=True)
   query = f"""UPDATE Products SET Price = {data["price"]} WHERE ProductID={id};"""
   response = sql(con,query)
   return f'Product with ID={id} successully updated, query: {query}', 200 


@api.route('/carts', methods=['GET'])
def get_carts():
    query = "SELECT * FROM Carts"
    response = sql(con,query)
    output = []
    for person_id, product_id in response.fetchall() :
        output.append({"person_id": person_id, "product_id": product_id})
    return json.dumps(output)

@api.route('/carts', methods=['POST'])
def add_products_in_carts():
    data = request.get_json(force=True)
    query = f"""INSERT INTO Carts VALUES({data["person_id"]},{data["product_id"]});"""
    sql(con,query)
    return f'Product successully added in cart , query: {query}', 200 


@api.route('/carts/<int:id>', methods=['GET'])
def get_cart_id(id):
   query = f"""SELECT * FROM Carts WHERE PersonID={id};"""
   response = sql(con,query)
   output = []
   for person_id, product_id in response.fetchall() :
        output.append({"person_id": person_id, "product_id": product_id})
   return json.dumps(output) 


@api.route('/carts/<int:id>', methods=['PUT'])
def put_cart_id(id):
   data = request.get_json(force=True)
   query = f"""INSERT INTO Carts VALUES({id},{data["product_id"]});"""
   response = sql(con,query)
   return f'Person with ID={id} successully added a product in cart, query: {query}', 200 


if __name__ == '__main__':
    #open_db_connection()
    api.run(debug=True, host='0.0.0.0')
    print('test')
    #con.close()