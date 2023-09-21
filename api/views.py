from rest_framework import viewsets

from api.serializers import PublicationSerializer, PlaceSerializer
from news.models import Publication
from places.models import Place


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    # TODO добавить доступ автору или админу, остальным только для чтения


class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
