from rest_framework import serializers
from .models import Device, Measurement, DeviceDimension, Due, Manufacturer, Dimension


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ('id', 'name', 'created_at')


class DimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dimension
        fields = ('id', 'name', 'created_at')


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'identnr', 'manufacturer', 'accessnr', 'version', 'status', 'type')


class DeviceDimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceDimension
        fields = ('id', 'dimension', 'device')


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('id', 'device_dimension', 'storagenr', 'tariff', 'subunit', 'value', 'date')


class DueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Due
        fields = ('id', 'device_dimension', 'storagenr', 'tariff', 'subunit', 'value', 'date')


# Get the data
class DeviceDataSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer(many=False, allow_null=True, required=True)
    class Meta:
        model = Device
        fields = ('id', 'identnr', 'manufacturer', 'accessnr', 'version', 'status', 'type')


class CsvDataSerializer(serializers.ModelSerializer):
    dimension = DimensionSerializer(many=False, allow_null=True, required=True)
    device = DeviceDataSerializer(many=False, allow_null=True, required=True)
    # measurement = MeasurementSerializer(many=True, allow_null=True, required=True)

    class Meta:
        model = DeviceDimension
        fields = ('id', 'dimension', 'device')


class CsvHeaderSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('date_time',
                  'device_id',
                  'device_manufacturer',
                  'device_type',
                  'device_version',
                  'dimension_measurement',
                  'dimension_measurement_value',
                  'dimension_due_value',
                  'dimension_due_date')
