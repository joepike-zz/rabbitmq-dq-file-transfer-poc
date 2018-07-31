import time

import pika

# as in send.py we need to connect to the rabbitmq server

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))

channel = connection.channel()

# we don't know if the queue has been created already ,so run following command which is
# idempotent
channel.queue_declare(queue='hello')

# this callback has been modfified from recieve.py to replicate a time-consuming process represented by
# the sleep function for every '.' in the message sent
# if the worker dies all unacknowledged tasks will be redelivered to other workers
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done"
    ch.basic_ack(delivery_tag =  method.delivery_tag))

# whenever a message is published to the queue, the callback function will be called. this
# particular callback function should receive messages from the 'hello' queue. this is the 'consumer'.
# modified from no_ack=True to the default false so that an acknowledgement is sent from the worker
# when a task has been completed. acknowledgement must be sent on the same channel as the message
channel.basic_consume(callback,
                      queue='hello'
                      )

# a never ending loop is entered which waits for data and runs callbacks when necessary
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
