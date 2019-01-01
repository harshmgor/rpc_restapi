#!/usr/bin/env python
import pika
import rpc_query as query
import json
import queue_configuration as config

params = pika.URLParameters(config.url)
connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue=config.queue_name)


def on_request(ch, method, props, body):

    data = json.loads(str(body)[2:-1])

    if data['method'] == 'get':
        response = query.get()
    elif data['method'] == 'post':
        response = query.post(data['title'], data['body'])
    elif data['method'] == 'put':
        response = query.put(data['id'], data['title'], data['body'])
    elif data['method'] == 'delete':
        response = query.delete(data['id'])
    else:
        response = "wrong api"

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=json.dumps(response)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(on_request, queue=config.queue_name)
channel.start_consuming()
