import uuid
from django.db import models

# Create your models here.
class Device(models.Model):

    TEMPERATURE_SENSOR = 'Temperature Sensor'
    VOLTAGE_METER = 'Voltage Meter'
    CURRENT_METER = 'Current Meter'
    POWER_METER = 'Power Meter'

    TYPES = (
        (TEMPERATURE_SENSOR, 'Temperature Sensor'),
        (VOLTAGE_METER, 'Voltage Meter'),
        (CURRENT_METER, 'Current Meter'),
        (POWER_METER, 'Power Meter'),
    )

    VOLTAGE = 1
    DEGREE = 2
    AMPERE = 3
    WATT = 4

    UNITS = (
        (VOLTAGE, 'V'),
        (DEGREE, '°C'),
        (AMPERE, 'A'),
        (WATT, 'W'),
    )

    id = models.CharField(primary_key=True, unique=True, max_length=128, null=False, blank=False)
    type = models.CharField(max_length=128, choices=TYPES, default=TEMPERATURE_SENSOR)
    unit = models.PositiveIntegerField(choices=UNITS, default=VOLTAGE)

    class Meta:
        db_table = 'devices'


class Record(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True, null=False, blank=False)
    record_time = models.PositiveIntegerField(null=False, blank=False)

    class Meta:
        db_table = 'records'



class DeviceRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey('Device', models.CASCADE, null=False, blank=False)
    record = models.ForeignKey('Record', models.CASCADE, null=False, blank=False)
    value = models.DecimalField(max_digits=11, decimal_places=3, default=0,)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'device_records'
