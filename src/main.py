#!/usr/bin/env python3
from json.tool import main
from flask import Flask, request
import pymysql
import time
import os
import json
import sys
import pika 
from flask_sqlalchemy import SQLAlchemy 
from config import settings

def get_db_password() -> str:
    try:
        db_password = open("/run/secrets/DB_PASSWORD", "r").read()
    except Exception as error:
        db_password = "admin"
        pass
    return db_password


retry = 10
while True:
    try:
        pymysql.install_as_MySQLdb()

        rabitmq_host = "ip-172-31-6-119" if os.getenv("SWARM") else "rabbitmq"

        api = Flask(__name__)

        host= "ip-172-31-6-119" if os.getenv("SWARM") else settings.hostname

        api.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{settings.user}:{str(get_db_password())}@{host}/{settings.db}'
    
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
        # RabbitMQ integration 
        break
    except BaseException as error:
        print("Error when connectiong to DB")
        time.sleep(retry*retry)
        retry-=1


@api.route('/add-job', methods=['POST'])
def add():
    data = request.get_json(force=True) # extract data from request 
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    connection.close()
    return {"status_code":200, "message": data}


# RabbitMQ finish integration 


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

@api.route('/persons', methods=['POST'])
def post_persons():
    data = request.get_json(force=True) # extract data from request 
    # query = f"""INSERT INTO Products VALUES({data["id"]},'{data["name"]}', {data["price"]});"""
    # sql(con,query)
    # return f'Product successully added, query: {query}', 200 
    person = Persons(
            PersonID=data["id"],
            LastName=data['name'],
        )
    db.session.add(person)
    db.session.commit()
    return "Person successfully added", 200


@api.route('/products', methods=['GET'])
def get_products():
    # query = "SELECT * FROM Products"
    # response = sql(con,query)
    output = []
    for product in Products.query.all():
        output.append({"id": product.ProductID, "name":product.ProductName, "price":product.Price})
    # for id, lastname, price in response.fetchall() :
    #     output.append({"id": id, "name": lastname, "price":price})
    # return json.dumps(output)
    return json.dumps(output)

@api.route('/products', methods=['POST'])
def post_products():
    data = request.get_json(force=True) # extract data from request 
    # query = f"""INSERT INTO Products VALUES({data["id"]},'{data["name"]}', {data["price"]});"""
    # sql(con,query)
    # return f'Product successully added, query: {query}', 200 
    product = Products(
            ProductID=data["id"],
            ProductName=data['name'],
            Price=data["price"]
        )
    db.session.add(product)
    db.session.commit()
    return "Product successfully added", 200



@api.route('/products/<int:id>', methods=['GET'])
def get_product_id(id):
#    query = f"""SELECT * FROM Products WHERE ProductID={id};"""
#    response = sql(con,query)
   output = []
   product = Products.query.filter_by(ProductID ={id}).first()
#    for id, lastname, price in response.fetchall() :
#         output.append({"id": id, "name": lastname, "price":price})
   output.append({"id": product.ProductID, "name":product.ProductName, "price":product.Price})
   return json.dumps(output) 


@api.route('/products/<int:id>', methods=['PUT'])
def put_product_id(id):
#    data = request.get_json(force=True)
#    query = f"""UPDATE Products SET Price = {data["price"]} WHERE ProductID={id};"""
#    response = sql(con,query)
#    return f'Product with ID={id} successully updated, query: {query}', 200 
    output=[]
    data = request.get_json(force=True)
    product = Products.query.filter_by(ProductID = {id}).first()
    product.Price = data["price"]
    db.session.commit()
    return f'Product with ID={id} sucesfully updated', 200



@api.route('/carts', methods=['GET'])
def get_carts():
    # query = "SELECT * FROM Carts"
    # response = sql(con,query)
    output = []
    # for person_id, product_id in response.fetchall() :
    #     output.append({"person_id": person_id, "product_id": product_id})
    output = []
    for cart in Carts.query.all():
        output.append({"PersonID": cart.PersonID, "ProductID": cart.ProductID})
    return json.dumps(output)


@api.route('/carts', methods=['POST'])
def add_products_in_carts():
    data = request.get_json(force=True)
    # query = f"""INSERT INTO Carts VALUES({data["person_id"]},{data["product_id"]});"""
    # sql(con,query)
    # return f'Product successully added in cart , query: {query}', 200 
    cart = Carts(
            ID = data["id"],
            PersonID = data["person_id"],
            ProductID = data["product_id"]          
    )
    db.session.add(cart)
    db.session.commit()
    return f"Product with id = {cart.ProductID} successfully added in cart", 200

@api.route('/carts/<int:id>', methods=['GET'])
def get_cart_id(id):
#    query = f"""SELECT * FROM Carts WHERE PersonID={id};"""
#    response = sql(con,query)
#    output = []
#    for person_id, product_id in response.fetchall() :
#         output.append({"person_id": person_id, "product_id": product_id})
#    return json.dumps(output) 
    output = []
    cart = Carts.query.filter_by(PersonID ={id}).first()
    output.append({"ID": cart.ID, "ProductID": cart.ProductID, "PersonID": cart.PersonID})
    return json.dumps(output)


@api.route('/carts/<int:id>', methods=['PUT'])
def put_cart_id(id):
#    data = request.get_json(force=True)
#    query = f"""INSERT INTO Carts VALUES({id},{data["product_id"]});"""
#    response = sql(con,query)
#    return f'Person with ID={id} successully added a product in cart, query: {query}', 200 
    cart = Carts.query.filter_by(PersonID = {id}).first()
    data = request.get_json(force=True)
    cart.ProductID = data["product_id"]
    db.session.commit()
    return f'Person with ID={id} successully added a product in cart', 200 

if __name__ == '__main__':
    #open_db_connection()
    api.run(debug=True, host='0.0.0.0')
    print('test')
    #con.close()