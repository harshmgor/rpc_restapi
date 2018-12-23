#!/usr/bin/env python
import pika
import api_request

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

url = "http://harshmgor.pythonanywhere.com/api/data/"
headers = {"Content-Type": "application/json"}


def on_request(ch, method, props, body):
    arg = str(body).split('/')
    if len(arg) > 1:
        if arg[0] == "b'get":
            print("api_get")
            response = api_request.api_get(url, headers)
        elif arg[0] == "b'post":
            print("api_post")
            response = api_request.api_post(url, arg[1:-1], headers)
        elif arg[0] == "b'put":
            print("api_put")
            response = api_request.api_put(url + arg[1] + "/", arg[2:-1], headers)
        elif arg[0] == "b'delete":
            print("api_delete")
            response = api_request.api_delete(url + arg[1] + "/")
        else:
            print("wrong api")
            print(body)
            print(arg)
            response = "wrong api"

    else:
        print("arguments missing")
        response = "arguments missing"

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=str(response)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(on_request, queue='rpc_queue')
print(" [x] Awaiting RPC requests")
channel.start_consuming()
