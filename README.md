# E-store application with Python, Flask and MySQL

## Set up:

### 1. Set-up local env: 
```
pip install --upgrade pip
python3 -m venv .venv
source .venv/bin/activate
pip install -r src/requirments.txt

```

If mysql_config is missing on your system:
sudo apt install default-libmysqlclient-dev 

### 2. Build docker image on local:
```
clean up old images:

   docker images
   docker rmi -f <images list ex:"mysql:5.7.22, mysql:latest">

build the new image with next tag:

  docker build . -t giuliaioana/python_flask_app:0.3
  docker images

```

### 3. Run all on local:

```
   docker-compose up -d

```

### 3. Check if is running as expected:

```
docker ps -a
docker logs app

curl http://localhost:5000/

```
Expected output:

```
127.0.0.1 - - [22/Oct/2021 17:55:53] "GET / HTTP/1.1" 404 -
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>

```

### 4. Requests examples: 

```
/products/ - GET, POST

GET: 
curl localhost:5000/products

POST: 
curl -X POST -H "Content-Type: application/json" -d '{"id": 4,"name": "pix", "price": "10"}' http://localhost:5000/products



/products/<product_id>/  - GET, PUT 

GET:
curl localhost:5000/products/1

PUT: 
curl -X PUT -H "Content-Type: application/json" -d '{"price": "100"}' http://localhost:5000/products/1



/shopping_carts/ - GET, POST 

GET: 
curl localhost:5000/carts

POST:
curl -X POST -H "Content-Type: application/json" -d '{"person_id": 2,"product_id": 1}' http://localhost:5000/carts



/shopping_carts/<cart_id>/ - GET, PUT

GET: 
curl localhost:5000/carts/1

PUT:
curl -X PUT -H "Content-Type: application/json" -d '{"product_id": "3"}' http://localhost:5000/carts/1

```

### 5. Using CLI: 

``` 
Examples of commands: 

If you want to get all the products from db: 
./cli.py -m "GET" -t "products" 

If you want to post products into db: 
./cli.py --method "POST" --table "products" --data '{"id": 41,"name": "pix", "price": 10}'

If you want to update a specific product from db:
./cli.py --method "PUT" --table "products" --id 2 --data '{"price": 1010}'

```