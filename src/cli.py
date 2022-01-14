#!/usr/bin/env python3
import json
import requests 
import argparse
import logging

logging.basicConfig(level=logging.INFO, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create the ArgumentParser object
parser = argparse.ArgumentParser(description='Query your db!')

# Adding arguments using add_argument() method 
parser.add_argument('-t','--table', help='Please provide a table name', default=None)
parser.add_argument('-m','--method', help='Please provide a http method name', default=None)
parser.add_argument('-i','--id', help='Please provide an ID for this request', default=None)
parser.add_argument('-d','--data', help='Please provide requested data', default=None, type=json.loads)

#Parse arguments through the parse_args() method 
args = parser.parse_args()

def call_request(table: str, id: str, data: dict, method: str = "GET") -> None:
    if (method == "GET") and (id == None):
        response = requests.get(f"http://127.0.0.1:5000/{table}")
        logger.info(response.content)
    elif (method == "POST") and (id == None):
        response = requests.post(f"http://127.0.0.1:5000/{table}", json=data)
        logger.info(response.content)
    if (method == "GET") and (id !=None):
        response = requests.get(f"http://127.0.0.1:5000/{table}/{id}")
        logger.info(response.content)
    if (method == "PUT") and (id !=None):
        response = requests.put(f"http://127.0.0.1:5000/{table}/{id}", json=data)
        logger.info(response.content)

    
call_request(args.table,args.id,args.data,args.method)

