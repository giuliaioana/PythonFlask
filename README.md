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

### 4. Run docker swarm 
```
Start docker swarm:
sudo docker swarm init --advertise-addr ip-172-31-4-85
```

```
Check nodes:
docker node ls
```

```
Leave swarm at the begining:
sudo docker swarm leave --force
```

```
Create docker secret:
echo "admin" | docker secret create DB_PASSWORD -
```

```
Deploy compose in stack:
docker stack deploy --compose-file swarm-deployments/mysql.yaml mysql && \
sleep 30 && \
docker stack deploy --compose-file swarm-deployments/app.yaml app && \
docker stack deploy --compose-file swarm-deployments/worker.yaml worker && \
docker stack deploy --compose-file swarm-deployments/rabbitmq.yaml rabbitmq && \
docker stack deploy --compose-file swarm-deployments/mysql_adminer.yaml mysql_adminer
```

```
Check docker compose status:
docker stack services stackdemo
```

```
Remove docker stack:
docker stack rm stackdemo
```

```
Add docker stack label:
docker node update --label-add BE=true ip-172-31-6-119
docker node update --label-add FE=true ip-172-31-7-35
```
### 5. Check if is running as expected:

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

### 6. Requests examples: 

Request sent to RabbitMQ and processed by worker: 
```
curl -X POST -H "Content-Type: application/json" -d '{"ProductID": 1114,"ProductName": "pix", "Price": 10}' http://172.31.7.35:5000/add-job
```
```
/products/ - GET, POST

GET: 
curl 172.31.7.35:5000/products

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

### 7. Using CLI: 

``` 
Examples of commands: 

If you want to get all the products from db: 
./cli.py -m "GET" -t "products" 

If you want to post products into db: 
./cli.py --method "POST" --table "products" --data '{"id": 41,"name": "pix", "price": 10}'

If you want to update a specific product from db:
./cli.py --method "PUT" --table "products" --id 2 --data '{"price": 1010}'

```

### 8. RabbitMQ

```
Run rabbitmq image: 
docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3.6-management-alpine

RabbitMQ management console:
http://locahost:15672
username and password : guest 

To send messages to broker: 
curl localhost:5000/add-job/hey

Expected output: 
[x] Sent: hey

Check the job result: 
docker logs giuliaioana/worker:latest

Expected output: 
 [*] Sleeping for  10  seconds.
 [*] Connecting to server ...
 [*] Waiting for messages.
 [x] Received b'hey'
hey there
 [x] Done

```