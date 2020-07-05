#!/usr/bin/env python3
"""
Import packages
"""
from django.core.management.base import BaseCommand
from metr.rabbitmq import RabbitMq


class Command(BaseCommand):
    """Commaand line argument to start rabbitMQ to consume data"""
    def add_arguments(self, parser):
        parser.add_argument('operation')

    def start(self):
        """
        python manage.py rmq start
        use to start consuming data from rabbitMQ queue broker
        :return:
        """
        self.stdout.write("RabbitMQ consumer started...")
        server = RabbitMq()
        server.startserver()

    def stop(self):
        """
        python manage.py rmq stop
        use to stop rabbitMQ queue broker
        currently not implemented
        :return:
        """
        self.stdout.write("RabbitMQ consumer stop.")

    def handle(self, *args, **options):
        """ Use to handle the argument on command line """
        operation = options.get("operation")
        if operation == 'start':
            self.start()
        elif operation == 'stop':
            self.stop()
        else:
            self.stdout.write("Invalid argument")
