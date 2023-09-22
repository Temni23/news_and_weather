import xlsxwriter
from rest_framework import viewsets
from django.http import HttpResponse
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.permissions import IsAuthorStaffOrReadOnly
from api.serializers import (PublicationSerializer, PlaceSerializer,
                             WeatherReportSerializer, CommentSerializer)
from news.models import Publication
from places.models import Place, WeatherReport

from datetime import datetime


class PublicationViewSet(viewsets.ModelViewSet):
    """Вьюст для публикаций."""
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthorStaffOrReadOnly,)


class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюст для памятных мест."""
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class WeatherReportViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюст для сводок с погодой."""
    queryset = WeatherReport.objects.all()
    serializer_class = WeatherReportSerializer
    filter_backends = [SearchFilter]
    search_fields = ['report_time']


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюст для комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorStaffOrReadOnly, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        id_comment = self.kwargs.get('publication_id')
        review = get_object_or_404(Publication, pk=id_comment,)
        serializer.save(review=review)

    def get_queryset(self):
        id_comment = self.kwargs.get('publication_id')
        new_queryset = get_object_or_404(Publication, pk=id_comment,)
        return new_queryset.comments.all()


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
