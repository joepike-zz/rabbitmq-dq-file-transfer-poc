
import pika

# as in send.py we need to connect to the rabbitmq server

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))

channel = connection.channel()

# we don't know if the queue has been created already ,so run following command which is
# idempotent
channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

# whenever a message is published to the queue, the callback function will be called. this
# particular callback function should receive messages from the 'hello' queue
channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

# a never ending loop is entered which waits for data and runs callbacks when necessary
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
