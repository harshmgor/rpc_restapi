#!usr/bin/env python
import pika
import uuid
import sys

url = 'amqp://dszgrpet:Yw5yKoMZqINvp78V63Su7Svw02KyhCcX@dinosaur.rmq.cloudamqp.com/dszgrpet'
params = pika.URLParameters(url)

class RpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            self.on_response,
            no_ack=True,
            queue=self.callback_queue
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, data):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(reply_to=self.callback_queue,correlation_id=self.corr_id),
            body=str(data)
        )
        while self.response is None:
            self.connection.process_data_events()
        return self.response


if len(sys.argv) > 1:
    rpc = RpcClient()
    print(" [x] Requesting " + sys.argv[1])
    response = rpc.call(sys.argv[1])
    print(" [.] Got %r" % response)
else:
    print("Arguments Missing")
