#!/usr/bin/env python3
"""
Import packages
"""
import uuid

from django.db import models
from django.utils import timezone


# Create your models here.
class Manufacturer(models.Model):
    """
    Model used for storing Manufacturer name
    """
    name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_at = models.DateField(null=True, blank=True, default=None)

    class Meta:
        """ Meta class used for making a relation with table"""
        db_table = "metr_manufacturer"


class Device(models.Model):
    """
    Model used for storing device information
    """
    identnr = models.IntegerField(default=0)
    manufacturer = models.ForeignKey(Manufacturer, related_name='device_manufacturer', null=True,
                                     on_delete=models.CASCADE)
    accessnr = models.IntegerField(default=0)
    version = models.IntegerField(default=0)
    status = models.BooleanField(default=0)
    type = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_at = models.DateField(null=True, blank=True, default=None)

    class Meta:
        """ Meta class used for making a relation with table"""
        db_table = "metr_device"


class Dimension(models.Model):
    """
    Model used for storing dimension name
    """
    name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_at = models.DateField(null=True, blank=True, default=None)

    class Meta:
        """ Meta class used for making a relation with table"""
        db_table = "metr_dimension"


class DeviceDimension(models.Model):
    """
    Model used for storing device dimension relation
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dimension = models.ForeignKey(Dimension, related_name='dd_dimension', null=True,
                                  on_delete=models.CASCADE)
    device = models.ForeignKey(Device, related_name='dd_device', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        """ Meta class used for making a relation with table"""
        db_table = "metr_device_dimension"

    def latest_measurement(self, year, month):
        """ Method for one to many relation with measurement data for latest data based on dimension """
        result = Measurement.objects.filter(device_dimension=self.id).\
            filter(date__year=year).filter(date__month=month).order_by('-date').first()

        return {
            'value': result.value if result else None,
            'date': result.date.strftime("%b %d %Y %H:%M:%S") if result else None,
        }

    def latest_measurement_value(self):
        """ Method to get value """
        if self.latest_measurement() is None:
            return None
        return self.latest_measurement().value

    def latest_measurement_date(self):
        """ Method to get date """
        if self.latest_measurement() is None:
            return None
        return self.latest_measurement().date.strftime("%b %d %Y %H:%M:%S")

    def latest_due(self, year, month):
        """ Method for one to many relation with due data for latest data based on dimension """
        result = Due.objects.filter(device_dimension=self.id).\
            filter(date__year=year).filter(date__month=month).order_by('-date').first()

        return {
            'value': result.value if result else None,
            'date': result.date.strftime("%b %d %Y %H:%M:%S") if result else None,
        }


    def latest_due_value(self):
        """ Method to get value """
        if self.latest_due() is None:
            return None
        return self.latest_due().value

    def latest_due_date(self):
        """ Method to get date """
        if self.latest_due() is None:
            return None
        return self.latest_due().date.strftime("%b %d %Y %H:%M:%S")

    def created_date(self):
        """ Method to get created date """
        return self.created_at.strftime("%b %d %Y %H:%M:%S")


class Measurement(models.Model):
    """
    Model used for storing metr recording provided by gatway
    Information contain relation with device and dimension
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_dimension = models.ForeignKey(DeviceDimension, related_name='measurement_dd', null=True,
                                         on_delete=models.CASCADE)
    storagenr = models.IntegerField(default=0)
    tariff = models.IntegerField(default=0)
    subunit = models.IntegerField(default=0)
    value = models.IntegerField(default=0)
    date = models.DateTimeField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        """ Meta class used for making a relation with table"""
        db_table = "metr_measurement"


class Due(models.Model):
    """
    Model used for storing pending data information
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_dimension = models.ForeignKey(DeviceDimension, related_name='due_dd', null=True,
                                         on_delete=models.CASCADE)
    storagenr = models.IntegerField(default=0)
    tariff = models.IntegerField(default=0)
    subunit = models.IntegerField(default=0)
    value = models.IntegerField(default=0)
    date = models.DateTimeField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        """ Meta class used for making a relation with table"""
        db_table = "metr_due"

