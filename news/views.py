from rest_framework import viewsets

from api.serializers import PublicationSerializer
from news.models import Publication


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
