from django.shortcuts import render
from django.http import Http404
import csv
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from .serializers import DeviceSerializer, MeasurementSerializer, DeviceDimensionSerializer, DueSerializer, \
    CsvDataSerializer, CsvHeaderSerializer
from .service import DataProcess
from .models import DeviceDimension


# Create your views here.

class DataList(APIView):
    """
    List all Data, or store new data record.
    """

    def get(self, request, format=None):
        # snippets = Snippet.objects.all()
        # serializer = SnippetSerializer(snippets, many=True)
        # return Response(serializer.data)
        return Response({}, status=status.HTTP_201_CREATED)

    def post(self, request, format=None):
        print("Requested:")
        # device = DeviceSerializer(data=request.data['device'])
        # if device.is_valid() is False:
        #     return Response(device.errors, status=status.HTTP_400_BAD_REQUEST)
        # device.save()
        data = DataProcess(request.data)
        for row in dict(data.get()):
            print(data.device)
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
            for row in data.slice_data[row]:
                print('insert', row)
                row.update({'device_dimension': dd.data.get('id')})
                print(row)
                if row['type'] == 'reading':
                    mesurement = MeasurementSerializer(data=row)
                    if mesurement.is_valid() is False:
                        return Response(mesurement.errors, status=status.HTTP_400_BAD_REQUEST)
                    mesurement.save()
                else:
                    due = DueSerializer(data=row)
                    if due.is_valid() is False:
                        return Response(due.errors, status=status.HTTP_400_BAD_REQUEST)
                    due.save()
        # for row in data.get_latest_data():
        #     print('insert', row)
        #     mesurement = MeasurementSerializer(data=row)
        #     if mesurement.is_valid() is False:
        #         return Response(mesurement.errors, status=status.HTTP_400_BAD_REQUEST)
        #     mesurement.save()
        # for row in data.get_due_date_data():
        #     print('insert', row)
        #     mesurement = MeasurementSerializer(data=row)
        #     if mesurement.is_valid() is False:
        #         return Response(mesurement.errors, status=status.HTTP_400_BAD_REQUEST)
        #     mesurement.save()
        response = {
            'message': 'Data saved sucessfully',
            'data': {
                'device': data.device.identnr,
                'version': data.device.version,
                'manufacturer': data.device.manufacturer.name
            }
        }
        return Response(response, status=status.HTTP_201_CREATED)


class CSVAPIView(ListAPIView):
    queryset = DeviceDimension.objects.all()

    serializer_class = CsvDataSerializer

    def get_queryset(self):
        queryset_list = DeviceDimension.objects.all()

        return queryset_list

    def get(self, request, format=None):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'

        # snippets = Snippet.objects.all()
        # serializer = SnippetSerializer(snippets, many=True)
        # return Response(serializer.data)
        list = []
        for row in self.get_queryset():
            list.append({
                'date_time': row.created_date(),
                'device_id': row.device.identnr,
                'device_manufacturer': row.device.manufacturer.name,
                'device_type': row.device.type,
                'device_version': row.device.version,
                'dimension_measurement': row.dimension.name,
                'dimension_measurement_value': row.latest_measurement_value(),
                'dimension_due_value': row.latest_due_value(),
                'dimension_due_date': row.latest_due_date(),
            })
        header = CsvHeaderSerializer.Meta.fields
        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
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
        # return Response(list, status=status.HTTP_201_CREATED)
