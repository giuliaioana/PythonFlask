import json
import requests 
from requests.exceptions import ConnectionError
import argparse

# Create the ArgumentParser object
parser = argparse.ArgumentParser(description='Query your db!')
# Adding arguments using add_argument() method 
parser.add_argument('method')

#Parse arguments through the parse_args() method 
args = parser.parse_args()
if args.method == 'get':
    r = requests.get('http://127.0.0.1:5000/products')
    print(r.status_code)
    print(r.content)
if args.method == 'post':
    r = requests.post('http://127.0.0.1:5000/products', json={"id": 4,"name": "pix", "price": "10"})
    print(r.status_code)
    print(r.content)
