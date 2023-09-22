from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import PublicationViewSet, PlaceViewSet, WeatherReportViewSet, \
    download_weather_data

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('news', PublicationViewSet, basename='news')
router_v1.register('places', PlaceViewSet, basename='places')
router_v1.register('weather', WeatherReportViewSet, basename='weather')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('download_weather_data/', download_weather_data,
         name='download_weather_data')
    # http://127.0.0.1:8000/api/download_weather_data/?date=2023-09-22&place_id=1
]
