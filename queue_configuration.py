#!usr/bin/env python
import pika

url = 'amqp://dszgrpet:Yw5yKoMZqINvp78V63Su7Svw02KyhCcX@dinosaur.rmq.cloudamqp.com/dszgrpet'
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)

# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
