from django.contrib import admin
from echo.models import Device, DeviceRecord, Record

# Register your models here.
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'unit')


class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'record_time')


class DeviceRecordAdmin(admin.ModelAdmin):
    list_display = ('device', 'record', 'value', 'created')


admin.site.register(Device, DeviceAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(DeviceRecord, DeviceRecordAdmin)

