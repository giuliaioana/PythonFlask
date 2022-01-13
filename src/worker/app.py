from shutil import ExecError
import pika
import time
import json
import pymysql.cursors

# Connect to the database
def get_con():
    mysq_connection = pymysql.connect(host='mysql',
                                user='admin',
                                password='admin',
                                database='main',
                                cursorclass=pymysql.cursors.DictCursor)
    return mysq_connection

sleepTime = 10
print(' [*] Sleeping for ', sleepTime, ' seconds.')
time.sleep(10)

print(' [*] Connecting to server ...')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

print(' [*] Waiting for messages.')


def callback(ch, method, properties, body):
    data = json.loads(body)
    print(type(data))
    print(f"Data is {data}")
    try:
        print("Init Connection")
        with get_con() as con:
            with con.cursor() as cursor:
                # Create a new record
                sql = f"""INSERT INTO `Products` (`ProductID`, `ProductName`, `Price`)
VALUES ({int(data.get("ProductID"))},"{str(data.get("ProductName"))}",{int(data.get("Price"))})"""
                cursor.execute(sql)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            con.commit()
            print("Commited")
    
    except Exception as error:
        print(repr(error))

    if data == 'hey':
        print("hey there")
    elif data == 'hello':
        print("well hello there")
    else:
        print("sorry i did not understand ", body)

    print(" [x] Done")

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()