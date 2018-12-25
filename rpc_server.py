#!/usr/bin/env python
import pika
import api_request
import json
import queue_configuration as config

params = pika.URLParameters(config.url)
connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue=config.queue_name)

url = config.server_url
headers = config.data_headers


def on_request(ch, method, props, body):
    arg = str(body).split('/')
    if len(arg) > 1:
        if arg[0] == "b'get":
            response = api_request.api_get(url, headers)
        elif arg[0] == "b'post":
            response = api_request.api_post(url, arg[1:-1], headers)
        elif arg[0] == "b'put":
            response = api_request.api_put(url + arg[1] + "/", arg[2:-1], headers)
        elif arg[0] == "b'delete":
            response = api_request.api_delete(url + arg[1] + "/")
        else:
            response = "wrong api"

    else:
        response = "arguments missing"

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=json.dumps(response)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(on_request, queue=config.queue_name)
channel.start_consuming()
