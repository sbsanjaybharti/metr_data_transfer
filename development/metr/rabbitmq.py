#!/usr/bin/env python3
"""
Import packages
"""
import os
import pika
import ast
from .service import MessageProcess

"""
RabbitMQ connection variable
"""
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_USERNAME = os.getenv('RABBITMQ_USERNAME')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')
RABBITMQ_ROUTINGKEY = os.getenv('RABBITMQ_ROUTINGKEY')
RABBITMQ_EXCHANGE = os.getenv('RABBITMQ_EXCHANGE')
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE')

class RabbitMq():

    def __init__(self):
        """ Configure Rabbit Mq Server  """
        credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(RABBITMQ_HOST, 5672, '/', credentials)
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=RABBITMQ_QUEUE)

    def callback(self, ch, method, properties, body):

        body = ast.literal_eval(body.decode("utf-8"))
        flag = MessageProcess(body).set()
        if flag is True:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def publish(self, payload={}):
        """
        :param payload: JSON payload
        :return: None
        """
        # print('========={}={}={}'.format(RABBITMQ_EXCHANGE, RABBITMQ_ROUTINGKEY, str(payload)))
        self._channel.basic_publish(exchange=RABBITMQ_EXCHANGE,
                                    routing_key=RABBITMQ_ROUTINGKEY,
                                    body=str(payload))

        print("Published Message: {}".format(payload))

    def close_connection(self):
        """
        :param payload: JSON payload
        :return: None
        """
        self._connection.close()

    def startserver(self):
        self._channel.basic_consume(
            queue=RABBITMQ_QUEUE,
            on_message_callback=self.callback,
            auto_ack=False)
        self._channel.start_consuming()
