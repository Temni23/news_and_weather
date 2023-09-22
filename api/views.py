from rest_framework import viewsets

from api.serializers import (PublicationSerializer, PlaceSerializer,
                             WeatherReportSerializer)
from news.models import Publication
from places.models import Place, WeatherReport


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
