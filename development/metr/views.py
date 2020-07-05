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
from .service import DataProcess
from .models import DeviceDimension


# Create your views here.
#
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
        data = DataProcess(request.data)
        for row in dict(data.get()):
            item = {
                'device': data.device.id,
                'dimension': row
            }
            dd = DeviceDimension.objects.filter(device=data.device.id, dimension=row).first()
            if dd:
                dd = DeviceDimensionSerializer(dd)
            else:
                dd = DeviceDimensionSerializer(data=item)
                if dd.is_valid() is False:
                    return Response(dd.errors, status=status.HTTP_400_BAD_REQUEST)
                dd.save()
            for item in data.slice_data[row]:
                item.update({'device_dimension': dd.data.get('id')})
                if item['type'] == 'reading':
                    mesurement = MeasurementSerializer(data=item)
                    if mesurement.is_valid() is False:
                        return Response(mesurement.errors, status=status.HTTP_400_BAD_REQUEST)
                    mesurement.save()
                else:
                    due = DueSerializer(data=item)
                    if due.is_valid() is False:
                        return Response(due.errors, status=status.HTTP_400_BAD_REQUEST)
                    due.save()

        response = {
            'message': 'Data saved sucessfully',
            'data': {
                'device': data.device.identnr,
                'version': data.device.version,
                'manufacturer': data.device.manufacturer.name
            }
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
