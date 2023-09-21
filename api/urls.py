from django.urls import include, path
from rest_framework.routers import DefaultRouter

from news.views import PublicationViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('news', PublicationViewSet, basename='news')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')), ]
