#!/usr/bin/env python3
"""
Import packages
"""
import csv
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from .serializers import MeasurementSerializer, DeviceDimensionSerializer, DueSerializer, \
    CsvDataSerializer, CsvHeaderSerializer
from .service import DataProcess, MessageProcess
from .models import DeviceDimension
from .rabbitmq import RabbitMq


# Create your views here.
class GatewayConnect(APIView):
    """
    Class use to read message from queue system
    """
    def get(self, request, format=None):
        """
        Start the server and process the queue
        :param request:
        :param format:
        :return:
        """
        server = RabbitMq()
        server.startserver()

        response_object = {
            'code': '200',
            'type': 'Response',
            'message': 'RadditMQ server started'
        }

        return Response(response_object, status=status.HTTP_201_CREATED)


class DataList(APIView):
    """
    Class controller to handle for insert the data in json form.
    """

    def get(self, request, format=None):
        """
        display the page
        :param request:
        :param format:
        :return:
        """
        return Response({}, status=status.HTTP_201_CREATED)

    def post(self, request, format=None):
        """
        Request json to process
        :param request:
        :param format:
        :return:
        """
        print(request.data)
        flag = MessageProcess(request.data).set()
        if flag is True:
            response = {
                'message': 'Data saved sucessfully',
            }
        else:
            response = {
                'message': 'Something went wrong',
            }

        return Response(response, status=status.HTTP_201_CREATED)


# class to convert data into CSV
class CSVAPIView(ListAPIView):
    """
    Generics view process to list the data into CSV
    """
    queryset = DeviceDimension.objects.all()

    serializer_class = CsvDataSerializer

    def get_queryset(self):
        """
        Query to get the data from device dimension
        :return:
        """
        queryset_list = DeviceDimension.objects.all()

        return queryset_list

    def get(self, request, format=None):
        """
        Converting json data into csv form
        :param request:
        :param format:
        :return:
        """
        # Setting csv http response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'

        # list = []
        # converting ORM data from json
        # for row in self.get_queryset():
        #     list.append({
        #         'date_time': row.created_date(),
        #         'device_id': row.device.identnr,
        #         'device_manufacturer': row.device.manufacturer.name,
        #         'device_type': row.device.type,
        #         'device_version': row.device.version,
        #         'dimension_measurement': row.dimension.name,
        #         'dimension_measurement_value': row.latest_measurement_value(),
        #         'dimension_due_value': row.latest_due_value(),
        #         'dimension_due_date': row.latest_due_date(),
        #     })

        # Setting csv header
        header = CsvHeaderSerializer.Meta.fields
        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()

        # Iteration process for each row
        for row in self.get_queryset():
            temp = {
                'date_time': row.created_date(),
                'device_id': row.device.identnr,
                'device_manufacturer': row.device.manufacturer.name,
                'device_type': row.device.type,
                'device_version': row.device.version,
                'dimension_measurement': row.dimension.name,
                'dimension_measurement_value': row.latest_measurement_value(),
                'dimension_due_value': row.latest_due_value(),
                'dimension_due_date': row.latest_due_date(),
            }
            writer.writerow(temp)

        return response
