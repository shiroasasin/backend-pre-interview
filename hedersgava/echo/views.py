from datetime import datetime

from echo.models import Device, Record, DeviceRecord
from echo.custom_xml_parser import CustomXMLParser
from echo.serializers import DataSerializer

from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response as response

# Create your views here.

@api_view(['POST'])
def echo(request):
    """
    Request json data and return it
    """
    if request.method == 'POST':
        data = request.data
        if data:
            return response(data, status=200, content_type=request.content_type)
        return response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST',])
@parser_classes((CustomXMLParser,))
def post_data(request):
    """
    Post data with content-type XML
    """
    if request.method == 'POST':
        data = request.data
        if data:
            device = data['devices']

            if not device:
                res = {'message': 'wrong format request data.'}
                return response(res, status=status.HTTP_400_BAD_REQUEST)

            for key, value in device.items():
                if value == Device.TEMPERATURE_SENSOR:
                    type = Device.TEMPERATURE_SENSOR
                    unit = Device.DEGREE
                elif value == Device.VOLTAGE_METER:
                    type = Device.VOLTAGE_METER
                    unit = Device.VOLTAGE
                elif value == Device.CURRENT_METER:
                    type = Device.CURRENT_METER
                    unit = Device.AMPERE
                elif value == Device.POWER_METER:
                    type = Device.POWER_METER
                    unit = Device.WATT
                else:
                    res = {'message': 'wrong device type.'}
                    return response(res, status=status.HTTP_400_BAD_REQUEST)

                Device.objects.update_or_create(id=key, type=type, unit=unit)

            id_record = data['id']
            record_time = data['record_time']
            if not id_record or not record_time:
                res = {'message': 'wrong format request data.',}
                return response(res, status=status.HTTP_400_BAD_REQUEST)

            record = Record(id=data['id'], record_time=data['record_time'])

            try:
                record.save()
            except Exception as e:
                res = {'message': 'failed.', 'err':e.args[0]}
                return response(res, status=status.HTTP_400_BAD_REQUEST)

            bulk_record = []

            for element in data['data']:
                rec_device = Device.objects.get(id=element['device'])
                bulk_record.append(DeviceRecord(device=rec_device,
                                                record=record,
                                                value=element['value'],
                                                ))

            try:
                DeviceRecord.objects.bulk_create(bulk_record)
            except Exception as e:
                res = {'message': 'failed.', 'err': e.args[0]}
                return response(res, status=status.HTTP_400_BAD_REQUEST)

            queryset = DeviceRecord.objects.filter(record=record)

            serializer = DataSerializer(queryset, many=True)

            return response(serializer.data, status=200, content_type="application/json")
        return response(status=status.HTTP_400_BAD_REQUEST)

    return response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_detail_record(request, id):
    """
    GET response in json. Client can fetch the data by date time
    with query params:
    /data/<id>/?date=YYYY-mmm-dd H:M:S
    """
    if request.method == 'GET':
        data = id
        date = request.query_params.get('date')
        if date:
            queryset = DeviceRecord.objects.filter(record=data, created__startswith=date)

            serializer = DataSerializer(queryset, many=True)

            return response(serializer.data, status=200)
        else:
            queryset = DeviceRecord.objects.filter(record=data)
            serializer = DataSerializer(queryset, many=True)

            return response(serializer.data, status=200)

        return response(status=status.HTTP_400_BAD_REQUEST)
