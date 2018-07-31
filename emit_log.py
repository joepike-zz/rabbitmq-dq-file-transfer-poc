# here we have no queue_declare - the workers had to be pointed to the same queue to consume the message
# being published

import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))

channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or 'info: Hello World!'

# server will generate an empty queue with random name. once consumer connection is closed, the queue should
# be deleted, therefore it is exclusive
result = channel.queue_declare(exclusive=True)

# previously exchange was default, so messages were routed to the queue given by routing_key,
# now the exchange is defined, so messages go to 'logs' exchange
channel.basic_publish(exchange='logs',
                      routing_key=''
                      body=message)

print(" [x] Sent %r" % message)

connection.close()
