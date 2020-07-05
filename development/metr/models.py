import uuid

from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_at = models.DateField(null=True, blank=True, default=None)

    class Meta:
        db_table = "metr_manufacturer"


class Device(models.Model):
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
        db_table = "metr_device"


class Dimension(models.Model):
    name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_at = models.DateField(null=True, blank=True, default=None)

    class Meta:
        db_table = "metr_dimension"


class DeviceDimension(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dimension = models.ForeignKey(Dimension, related_name='dd_dimension', null=True,
                                  on_delete=models.CASCADE)
    device = models.ForeignKey(Device, related_name='dd_device', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        db_table = "metr_device_dimension"

    def latest_measurement(self):
        return Measurement.objects.filter(device_dimension=self.id).order_by('-date').first()

    def latest_measurement_value(self):
        if self.latest_measurement() is None:
            return None
        return self.latest_measurement().value

    def latest_measurement_date(self):
        if self.latest_measurement() is None:
            return None
        return self.latest_measurement().date.strftime("%b %d %Y %H:%M:%S")

    def latest_due(self):
        return Due.objects.filter(device_dimension=self.id).order_by('-date').first()

    def latest_due_value(self):
        if self.latest_due() is None:
            return None
        return self.latest_due().value

    def latest_due_date(self):
        if self.latest_due() is None:
            return None
        return self.latest_due().date.strftime("%b %d %Y %H:%M:%S")

    def created_date(self):
        return self.created_at.strftime("%b %d %Y %H:%M:%S")


class Measurement(models.Model):
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
        db_table = "metr_measurement"


class Due(models.Model):
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
        db_table = "metr_due"
#
# class Recording(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     collection_date = models.ForeignKey(CollectionDate, related_name='Recording_collection_date', null=True,
#                                         on_delete=models.CASCADE)
#     date = models.DateField(null=True, blank=True, default=None)
#     storagenr = models.IntegerField(default=0)
#     tariff = models.IntegerField(default=0)
#     subunit = models.IntegerField(default=0)
#     created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
#
#     class Meta:
#         db_table = "metr_recording"
