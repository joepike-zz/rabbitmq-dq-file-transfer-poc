
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))

channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

result = channel.queue_declare()
queue_name = result.method.queue

# we will add messages through the exchange 'logs' to the randomly named queue previously generated
channel.queue_bind(exchange='logs',
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(properties, ch, method, body):
    print(" [x] %r" % body)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True
                      )
