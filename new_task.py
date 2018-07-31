import sys

# initially ran into error 61 connection failed when trying to connect to a broker
# on the localhost. this is because needed to 'brew install rabbitmq', then run
# 'brew services start rabbitmq'

import pika

# this will open a connection to a broker on the localhost. 'localhost' can be
# changed to connect to a broker on another ip address.
# these two lines will establish a connection to the rabbitmq server.
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))

channel = connection.channel()

# make sure that the recipient queue exists. message will be delivered to this
# queue
channel.queue_declare(queue='hello', durable=True)

channel.queue_declare(queue='task_queue', durable=True)

# messages will not be published directly to a queue, they need to go through
# an exchange. the following uses a default exchange. the default exchange allows
# the recipient queue to be defined (routing_key)

# the following has been modified from send.py to publish a message to the queue with
# command line arguments.
# we will mark this message as persistent so that it is saved to disk and publish to
# a new queue task_queue
message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                        delivery_mode = 2,  # make message persistent
                      ))

print(" [x] Sent %r" % message)

connection.close()
