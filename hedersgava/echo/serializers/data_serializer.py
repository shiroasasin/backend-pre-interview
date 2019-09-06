from echo.models import Device, Record, DeviceRecord
from rest_framework import serializers

class DataSerializer(serializers.Serializer):
    datetime = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    unit = serializers.SerializerMethodField()

    def get_datetime(self, obj):
        datetime = obj.created
        return datetime.isoformat()

    def get_value(self, obj):
        value = obj.device.id
        return value

    def get_unit(self, obj):
        unit = obj.device.unit
        for u in Device.UNITS:
            if unit == u[0]:
                return u[1]
        return '-'

    class Meta:
        model = DeviceRecord
        fields = ('datetime', 'value', 'unit')