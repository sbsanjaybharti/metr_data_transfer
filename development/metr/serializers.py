#!/usr/bin/env python3
"""
Import packages
"""
from rest_framework import serializers
from .models import Device, Measurement, DeviceDimension, Due, Manufacturer, Dimension


class ManufacturerSerializer(serializers.ModelSerializer):
    """
    Manufacturer Serializer for manufecturer model
    """

    class Meta:
        """ Meta class with model and fields """
        model = Manufacturer
        fields = ('id', 'name', 'created_at')


class DimensionSerializer(serializers.ModelSerializer):
    """
    Dimension Serializer for dimension model
    """

    class Meta:
        """ Meta class with model and fields """
        model = Dimension
        fields = ('id', 'name', 'created_at')


class DeviceSerializer(serializers.ModelSerializer):
    """
    Device Serializer for device model
    """

    class Meta:
        """ Meta class with model and fields """
        model = Device
        fields = ('id', 'identnr', 'manufacturer', 'accessnr', 'version', 'status', 'type')


class DeviceDimensionSerializer(serializers.ModelSerializer):
    """
    Device dimension Serializer for relational model devicedimension
    """

    class Meta:
        """ Meta class with model and fields """
        model = DeviceDimension
        fields = ('id', 'dimension', 'device')


class MeasurementSerializer(serializers.ModelSerializer):
    """
    Measurement Serializer for measurement model
    """

    class Meta:
        """ Meta class with model and fields """
        model = Measurement
        fields = ('id', 'device_dimension', 'storagenr', 'tariff', 'subunit', 'value', 'date')


class DueSerializer(serializers.ModelSerializer):
    """
    Manufacturer Serializer for manufecturer model
    """

    class Meta:
        """ Meta class with model and fields """
        model = Due
        fields = ('id', 'device_dimension', 'storagenr', 'tariff', 'subunit', 'value', 'date')


# Get the data
class DeviceDataSerializer(serializers.ModelSerializer):
    """
    DeviceData Serializer is child serializer of CSVData serializer
    """
    manufacturer = ManufacturerSerializer(many=False, allow_null=True, required=True)

    class Meta:
        """ Meta class with model and fields """
        model = Device
        fields = ('id', 'identnr', 'manufacturer', 'accessnr', 'version', 'status', 'type')


class CsvDataSerializer(serializers.ModelSerializer):
    """
    CsvData Serializer is parent serializer to creating CSV data
    """
    dimension = DimensionSerializer(many=False, allow_null=True, required=True)
    device = DeviceDataSerializer(many=False, allow_null=True, required=True)

    # measurement = MeasurementSerializer(many=True, allow_null=True, required=True)

    class Meta:
        """ Meta class with model and fields """
        model = DeviceDimension
        fields = ('id', 'dimension', 'device')


class CsvHeaderSerializer(serializers.ModelSerializer):
    """
    CsvHeader Serializer for CSV header
    """

    class Meta:
        """ Meta class with model and fields """
        fields = ('date_time',
                  'device_id',
                  'device_manufacturer',
                  'device_type',
                  'device_version',
                  'dimension_measurement',
                  'dimension_measurement_value',
                  'dimension_due_value',
                  'dimension_due_date')
