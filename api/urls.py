from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import PublicationViewSet, PlaceViewSet, WeatherReportViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('news', PublicationViewSet, basename='news')
router_v1.register('places', PlaceViewSet, basename='places')
router_v1.register('weather', WeatherReportViewSet, basename='weather')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')), ]
