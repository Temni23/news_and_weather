import xlsxwriter
from rest_framework import viewsets
from django.http import HttpResponse

from api.serializers import (PublicationSerializer, PlaceSerializer,
                             WeatherReportSerializer)
from news.models import Publication
from places.models import Place, WeatherReport

from datetime import datetime


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    # TODO добавить доступ автору или админу, остальным только для чтения


class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    # TODO добавить фильтры по месту и времени


class WeatherReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WeatherReport.objects.all()
    serializer_class = WeatherReportSerializer


def download_weather_data(request):
    """По GET запросу пользователя генерирует эксель файл с данными о погоде"""
    if request.method == 'GET':
        date = request.GET.get('date')
        place_id = request.GET.get('place_id')
        date = datetime.strptime(date, '%Y-%m-%d')
        weather_data = WeatherReport.objects.filter(report_time__date=date,
                                                    place_id=place_id)
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.'
                         'spreadsheetml.sheet')
        response[
            'Content-Disposition'] = (f'attachment; '
                                      f'filename=weather_report_{date}.xlsx')

        workbook = xlsxwriter.Workbook(response, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        row = 0
        col = 0
        # Заголовки столбцов
        worksheet.write(row, col, 'Температура (°C)')
        worksheet.write(row, col + 1, 'Влажность (%)')
        worksheet.write(row, col + 2, 'Атмосферное давление (мм рт. ст.)')
        worksheet.write(row, col + 3, 'Место')
        for data in weather_data:
            row += 1
            worksheet.write(row, col, data.temperature)
            worksheet.write(row, col + 1, data.humidity)
            worksheet.write(row, col + 2, data.pressure)
            worksheet.write(row, col + 3, data.place.name)
        workbook.close()
        return response


